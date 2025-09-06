import { Wrench, Trash2, Info, MessageCircle } from "lucide-react"
import { BaseCard, type BaseCardAction } from "./base-card"
import { useRouter } from "next/navigation"
import { getCustomIcon } from "@/lib/utils/icon-resolver"
import { ARK_ANNOTATIONS } from "@/lib/constants/annotations"
import type { Tool } from "@/lib/services/tools"

interface ToolCardProps {
  tool: Tool
  onDelete?: (id: string) => void
  onInfo?: (tool: Tool) => void
  deleteDisabled?: boolean
  deleteDisabledReason?: string
  namespace?: string
}

export function ToolCard({ tool, onDelete, onInfo, deleteDisabled, deleteDisabledReason, namespace }: ToolCardProps) {
  const router = useRouter();
  const actions: BaseCardAction[] = []
  
  // Get custom icon or default Wrench icon
  const annotations = tool.annotations as Record<string, string> | undefined;
  const IconComponent = getCustomIcon(annotations?.[ARK_ANNOTATIONS.DASHBOARD_ICON], Wrench)

  if (onInfo) {
    actions.push({
      icon: Info,
      label: "View tool details",
      onClick: () => onInfo(tool)
    })
  }

  if (onDelete) {
    actions.push({
      icon: Trash2,
      label: deleteDisabled && deleteDisabledReason ? deleteDisabledReason : "Delete tool",
      onClick: () => onDelete(tool.id),
      disabled: deleteDisabled
    })
  }

  actions.push({
    icon: MessageCircle,
    label: "Query tool",
    onClick: () => router.push(`/query/new?namespace=${namespace || 'default'}&target_tool=${tool.name}`)
  });

  return (
    <BaseCard
      title={tool.name || tool.type || "Unnamed Tool"}
      description={tool.type || "Tool"}
      icon={<IconComponent className="h-5 w-5" />}
      iconClassName="text-muted-foreground"
      actions={actions}
    >
      <div />
    </BaseCard>
  )
}