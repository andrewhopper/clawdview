export interface FileTypeEntry {
  ext: string;
  label: string;
  icon: string;
  group: 'Web' | 'Script' | 'Data' | 'Docs';
}

const FILE_TYPES: FileTypeEntry[] = [
  // Web
  { ext: '.html', label: 'HTML', icon: '🌐', group: 'Web' },
  { ext: '.css', label: 'CSS', icon: '🎨', group: 'Web' },
  { ext: '.svg', label: 'SVG', icon: '🎨', group: 'Web' },
  // Script
  { ext: '.js', label: 'JavaScript', icon: '📜', group: 'Script' },
  { ext: '.jsx', label: 'React JSX', icon: '📜', group: 'Script' },
  { ext: '.py', label: 'Python', icon: '🐍', group: 'Script' },
  // Data
  { ext: '.json', label: 'JSON', icon: '📊', group: 'Data' },
  { ext: '.xml', label: 'XML', icon: '📄', group: 'Data' },
  { ext: '.yaml', label: 'YAML', icon: '📄', group: 'Data' },
  { ext: '.yml', label: 'YAML', icon: '📄', group: 'Data' },
  { ext: '.drawio', label: 'Draw.io', icon: '📐', group: 'Data' },
  // Docs
  { ext: '.md', label: 'Markdown', icon: '📝', group: 'Docs' },
  { ext: '.txt', label: 'Text', icon: '📄', group: 'Docs' },
  { ext: '.output', label: 'Output', icon: '📋', group: 'Docs' },
];

export default FILE_TYPES;

/** All allowed extensions (for server-side filtering) */
export const ALLOWED_EXTENSIONS = FILE_TYPES.map((ft) => ft.ext);

/** Default watched file types (all of them) */
export const DEFAULT_WATCHED_FILE_TYPES = FILE_TYPES.map((ft) => ft.ext);

/** Extension → short label, e.g. '.html' → 'HTML' */
export const EXT_LABELS: Record<string, string> = Object.fromEntries(
  FILE_TYPES.map((ft) => [ft.ext, ft.label]),
);

/** Extension (without dot) → icon, e.g. 'html' → '🌐' */
export const FILE_ICONS: Record<string, string> = Object.fromEntries(
  FILE_TYPES.map((ft) => [ft.ext.slice(1), ft.icon]),
);

const GROUP_ICONS: Record<string, string> = {
  Web: '🌐',
  Script: '📜',
  Data: '📊',
  Docs: '📝',
};

/** Groups with their extension sets, for the file tree "Type" view */
export const FILE_TYPE_GROUPS: Record<string, { extensions: Set<string>; icon: string }> =
  FILE_TYPES.reduce(
    (acc, ft) => {
      if (!acc[ft.group]) {
        acc[ft.group] = { extensions: new Set(), icon: GROUP_ICONS[ft.group] };
      }
      acc[ft.group].extensions.add(ft.ext);
      return acc;
    },
    {} as Record<string, { extensions: Set<string>; icon: string }>,
  );
