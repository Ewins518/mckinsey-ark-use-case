import { Lock, Pencil, Trash2 } from "lucide-react"
import { BaseCard, type BaseCardAction } from "./base-card"
import type { Secret } from "@/lib/services/secrets"
import type { Model } from "@/lib/services/models"

interface SecretCardProps {
  secret: Secret
  models: Model[]
  onEdit?: (secret: Secret) => void
  onDelete?: (id: string) => void
}

function modelUsesSecret(model: Model, secretName: string): boolean {
  const config = model.config
  if (!config) return false

  const checkValueSource = (valueSource: unknown): boolean => {
    if (!valueSource || typeof valueSource !== 'object') return false
    const source = valueSource as Record<string, unknown>
    const valueFrom = source.valueFrom as Record<string, unknown> | undefined
    const secretKeyRef = valueFrom?.secretKeyRef as Record<string, unknown> | undefined
    if (secretKeyRef?.name === secretName) return true
    return false
  }

  for (const [, providerConfig] of Object.entries(config)) {
    if (!providerConfig || typeof providerConfig !== 'object') continue
    
    for (const [, value] of Object.entries(providerConfig)) {
      if (checkValueSource(value)) return true
    }
  }

  return false
}

export function SecretCard({ secret, models, onEdit, onDelete }: SecretCardProps) {
  // Count models using this secret
  const modelsUsingSecret = models.filter(model => modelUsesSecret(model, secret.name))
  const usageCount = modelsUsingSecret.length
  const isInUse = usageCount > 0

  const actions: BaseCardAction[] = []

  if (onEdit) {
    actions.push({
      icon: Pencil,
      label: "Edit secret",
      onClick: () => onEdit(secret)
    })
  }

  if (onDelete) {
    actions.push({
      icon: Trash2,
      label: "Delete secret",
      onClick: () => onDelete(secret.id),
      disabled: isInUse
    })
  }

  return (
    <BaseCard
      title={secret.name}
      description={`Used by ${usageCount} model${usageCount !== 1 ? 's' : ''}`}
      icon={Lock}
      iconClassName="text-muted-foreground"
      actions={actions}
    >
      <div />
    </BaseCard>
  )
}