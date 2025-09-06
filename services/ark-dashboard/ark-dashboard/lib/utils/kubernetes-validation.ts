export function isValidKubernetesName(name: string): boolean {
  if (!name || name.length === 0 || name.length > 253) {
    return false;
  }

  // Safe regex pattern avoiding nested quantifiers that could cause ReDoS
  // Check start/end characters separately to avoid backtracking
  if (!/^[a-z0-9]/.test(name)) {
    return false;
  }
  if (!/[a-z0-9]$/.test(name)) {
    return false;
  }
  // Check that all characters are valid
  if (!/^[a-z0-9-]+$/.test(name)) {
    return false;
  }

  return true;
}

export function getKubernetesNameError(name: string): string | null {
  if (!name || name.length === 0) {
    return "Name is required";
  }

  if (name.length > 253) {
    return "Name must be 253 characters or less";
  }

  // Check if the first character is not alphanumeric (including uppercase)
  if (!/^[a-zA-Z0-9]/.test(name)) {
    return "Name must start with a lowercase letter or number";
  }

  // Check if the last character is not alphanumeric (including uppercase)
  if (!/[a-zA-Z0-9]$/.test(name)) {
    return "Name must end with a lowercase letter or number";
  }

  // Check if name contains only valid characters
  if (!/^[a-z0-9-]+$/.test(name)) {
    return "Name can only contain lowercase letters, numbers, and hyphens";
  }

  return null;
}
