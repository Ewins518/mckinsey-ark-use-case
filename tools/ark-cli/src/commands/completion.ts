import chalk from 'chalk';
import { Command } from 'commander';

export function createCompletionCommand(): Command {
  const completion = new Command('completion');
  completion.description('Generate shell completion scripts').action(() => {
    console.log(chalk.cyan('Shell completion for ARK CLI'));
    console.log('');
    console.log('Usage:');
    console.log('  ark completion bash   Generate bash completion script');
    console.log('  ark completion zsh    Generate zsh completion script');
    console.log('');
    console.log('To enable completion, add this to your shell profile:');
    console.log(chalk.grey('  # For bash:'));
    console.log(chalk.grey('  eval "$(ark completion bash)"'));
    console.log(chalk.grey('  # For zsh:'));
    console.log(chalk.grey('  eval "$(ark completion zsh)"'));
  });

  completion
    .command('bash')
    .description('Generate bash completion script')
    .action(() => {
      console.log(
        `
_ark_completion() {
  local cur prev opts
  COMPREPLY=()
  cur="\${COMP_WORDS[COMP_CWORD]}"
  prev="\${COMP_WORDS[COMP_CWORD-1]}"
  
  case \${COMP_CWORD} in
    1)
      opts="cluster completion check help"
      COMPREPLY=( $(compgen -W "\${opts}" -- \${cur}) )
      return 0
      ;;
    2)
      case \${prev} in
        cluster)
          opts="get-ip get-type"
          COMPREPLY=( $(compgen -W "\${opts}" -- \${cur}) )
          return 0
          ;;
        completion)
          opts="bash zsh"
          COMPREPLY=( $(compgen -W "\${opts}" -- \${cur}) )
          return 0
          ;;
        check)
          opts="status"
          COMPREPLY=( $(compgen -W "\${opts}" -- \${cur}) )
          return 0
          ;;
      esac
      ;;
  esac
}

complete -F _ark_completion ark
      `.trim()
      );
    });

  completion
    .command('zsh')
    .description('Generate zsh completion script')
    .action(() => {
      console.log(
        `
#compdef ark

_ark() {
  local context state line
  
  _arguments -C \\
    '1:command:->command' \\
    '2:subcommand:->subcommand' \\
    '*::arg:->args'
    
  case $state in
    command)
      _values 'ark commands' \\
        'cluster[Cluster management commands]' \\
        'completion[Generate shell completion scripts]' \\
        'check[Check system components]' \\
        'help[Show help information]'
      ;;
    subcommand)
      case $words[2] in
        cluster)
          _values 'cluster commands' \\
            'get-ip[Get cluster IP address]' \\
            'get-type[Get cluster type]'
          ;;
        completion)
          _values 'completion shells' \\
            'bash[Generate bash completion]' \\
            'zsh[Generate zsh completion]'
          ;;
        check)
          _values 'check commands' \\
            'status[Check system status]'
          ;;
      esac
      ;;
  esac
}

_ark
      `.trim()
      );
    });

  return completion;
}
