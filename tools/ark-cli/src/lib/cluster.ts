import { executeCommand } from './exec.js';

export interface ClusterInfo {
  type: 'minikube' | 'kind' | 'k3s' | 'docker-desktop' | 'cloud' | 'unknown';
  ip?: string;
  context?: string;
  error?: string;
}

export async function detectClusterType(): Promise<ClusterInfo> {
  try {
    const { stdout } = await executeCommand('kubectl', [
      'config',
      'current-context',
    ]);
    const context = stdout.trim();

    if (context.includes('minikube')) {
      return { type: 'minikube', context };
    } else if (context.includes('kind')) {
      return { type: 'kind', context };
    } else if (context.includes('k3s')) {
      return { type: 'k3s', context };
    } else if (context.includes('docker-desktop')) {
      return { type: 'docker-desktop', context };
    } else if (
      context.includes('gke') ||
      context.includes('eks') ||
      context.includes('aks')
    ) {
      return { type: 'cloud', context };
    } else {
      return { type: 'unknown', context };
    }
  } catch (error: any) {
    return { type: 'unknown', error: error.message };
  }
}

export async function getClusterIp(_context?: string): Promise<ClusterInfo> {
  try {
    const clusterInfo = await detectClusterType();

    if (clusterInfo.error) {
      return clusterInfo;
    }

    let ip: string | undefined;

    switch (clusterInfo.type) {
      case 'minikube':
        try {
          const { stdout } = await executeCommand('minikube', ['ip']);
          ip = stdout.trim();
        } catch {
          // Fallback to kubectl if minikube command fails
          const { stdout } = await executeCommand('kubectl', [
            'get',
            'nodes',
            '-o',
            'jsonpath={.items[0].status.addresses[?(@.type=="InternalIP")].address}',
          ]);
          ip = stdout.trim();
        }
        break;

      case 'kind': {
        const { stdout: kindOutput } = await executeCommand('kubectl', [
          'get',
          'nodes',
          '-o',
          'jsonpath={.items[0].status.addresses[?(@.type=="InternalIP")].address}',
        ]);
        ip = kindOutput.trim();
        break;
      }

      case 'docker-desktop':
        ip = 'localhost';
        break;

      case 'k3s': {
        const { stdout: k3sOutput } = await executeCommand('kubectl', [
          'get',
          'nodes',
          '-o',
          'jsonpath={.items[0].status.addresses[?(@.type=="InternalIP")].address}',
        ]);
        ip = k3sOutput.trim();
        break;
      }

      case 'cloud':
        // For cloud clusters, try to get the external IP or load balancer IP
        try {
          const { stdout: lbOutput } = await executeCommand('kubectl', [
            'get',
            'svc',
            '-n',
            'istio-system',
            'istio-ingressgateway',
            '-o',
            'jsonpath={.status.loadBalancer.ingress[0].ip}',
          ]);
          ip = lbOutput.trim();
          if (!ip) {
            const { stdout: hostnameOutput } = await executeCommand('kubectl', [
              'get',
              'svc',
              '-n',
              'istio-system',
              'istio-ingressgateway',
              '-o',
              'jsonpath={.status.loadBalancer.ingress[0].hostname}',
            ]);
            ip = hostnameOutput.trim();
          }
        } catch {
          // Fallback to node IP
          const { stdout: nodeOutput } = await executeCommand('kubectl', [
            'get',
            'nodes',
            '-o',
            'jsonpath={.items[0].status.addresses[?(@.type=="ExternalIP")].address}',
          ]);
          ip = nodeOutput.trim();
        }
        break;

      default: {
        const { stdout: defaultOutput } = await executeCommand('kubectl', [
          'get',
          'nodes',
          '-o',
          'jsonpath={.items[0].status.addresses[?(@.type=="InternalIP")].address}',
        ]);
        ip = defaultOutput.trim();
        break;
      }
    }

    return { ...clusterInfo, ip };
  } catch (error: any) {
    return { type: 'unknown', error: error.message };
  }
}
