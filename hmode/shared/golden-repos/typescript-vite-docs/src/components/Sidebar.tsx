// File UUID: c9d0e1f2-3a4b-5c6d-7e8f-9a0b1c2d3e4f
import { ScrollArea } from './ui/scroll-area'
import { Separator } from './ui/separator'
import { NavItem } from '@/lib/types'
import { cn } from '@/lib/utils'
import { FileText } from 'lucide-react'

interface SidebarProps {
  navItems: NavItem[]
  currentSlug: string | null
  onNavigate: (slug: string) => void
}

export function Sidebar({ navItems, currentSlug, onNavigate }: SidebarProps) {
  return (
    <div className="h-screen w-64 border-r bg-background">
      <div className="p-6">
        <h2 className="text-lg font-semibold">Documentation</h2>
        <p className="text-sm text-muted-foreground mt-1">
          Project documentation site
        </p>
      </div>

      <Separator />

      <ScrollArea className="h-[calc(100vh-120px)]">
        <nav className="p-4 space-y-1">
          {navItems.map((item) => (
            <button
              key={item.slug}
              onClick={() => onNavigate(item.slug)}
              className={cn(
                "w-full flex items-center gap-2 px-3 py-2 text-sm rounded-md transition-colors text-left",
                currentSlug === item.slug
                  ? "bg-secondary text-secondary-foreground font-medium"
                  : "hover:bg-secondary/50 text-foreground"
              )}
            >
              <FileText className="h-4 w-4 shrink-0" />
              <span className="truncate">{item.title}</span>
            </button>
          ))}

          {navItems.length === 0 && (
            <div className="px-3 py-8 text-center text-sm text-muted-foreground">
              No documentation files found.
              <br />
              Add .md files to the docs/ directory.
            </div>
          )}
        </nav>
      </ScrollArea>
    </div>
  )
}
