"""ARK services utilities for Helm release management."""
import logging
from typing import List, Dict, Any

from pyhelm3 import Client

logger = logging.getLogger(__name__)


async def _extract_chart_metadata(chart_metadata_obj) -> Dict[str, Any]:
    """Extract chart metadata from chart metadata object."""
    metadata = {'annotations': {}}
    
    if not chart_metadata_obj:
        return metadata
    
    # Extract annotations
    if hasattr(chart_metadata_obj, 'annotations') and chart_metadata_obj.annotations:
        metadata['annotations'] = chart_metadata_obj.annotations
    
    # Extract description
    if hasattr(chart_metadata_obj, 'description') and chart_metadata_obj.description:
        metadata['description'] = chart_metadata_obj.description
    
    return metadata


async def _get_revision_timestamp(revision) -> str:
    """Get timestamp from revision object."""
    if not revision:
        return ""
    
    # pyhelm3 revision objects use 'updated' field for timestamps
    if hasattr(revision, 'updated') and revision.updated:
        try:
            return revision.updated.isoformat() if hasattr(revision.updated, 'isoformat') else str(revision.updated)
        except Exception as e:
            logger.warning(f"Error processing updated timestamp: {e}")
    
    return ""


async def extract_helm_release_data(release) -> Dict[str, Any]:
    """Extract data from a Helm release object."""
    revision = await release.current_revision()
    chart_metadata_obj = await revision.chart_metadata()
    
    chart_name = chart_metadata_obj.name if chart_metadata_obj else ""
    chart_version = chart_metadata_obj.version if chart_metadata_obj else ""
    app_version = chart_metadata_obj.app_version if chart_metadata_obj else ""
    
    chart_metadata = await _extract_chart_metadata(chart_metadata_obj)
    updated_time = await _get_revision_timestamp(revision)
    
    return {
        'name': release.name,
        'namespace': release.namespace,
        'chart': f"{chart_name}-{chart_version}" if chart_name and chart_version else "",
        'chart_version': chart_version,
        'app_version': app_version,
        'status': str(revision.status),
        'revision': revision.revision,
        'updated': updated_time,
        'chart_metadata': chart_metadata
    }


async def get_helm_releases(namespace: str) -> List[Dict[str, Any]]:
    """Get Helm releases in a namespace using pyhelm3."""
    try:
        helm_client = Client()
        releases = await helm_client.list_releases(namespace=namespace)
        
        release_list = []
        for release in releases:
            release_data = await extract_helm_release_data(release)
            release_list.append(release_data)
        
        return release_list
        
    except Exception as e:
        logger.warning(f"Failed to get Helm releases for namespace {namespace}: {e}")
        return []


def get_chart_annotations(release_data: Dict[str, Any]) -> Dict[str, str]:
    """Get chart annotations from Helm release data."""
    chart_metadata = release_data.get('chart_metadata', {})
    return chart_metadata.get('annotations', {})


def get_chart_description(release_data: Dict[str, Any]) -> str:
    """Get chart description from Helm release data."""
    chart_metadata = release_data.get('chart_metadata', {})
    return chart_metadata.get('description', "")