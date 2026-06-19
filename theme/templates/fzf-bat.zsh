# ~/.config/theme/fzf-bat.zsh
# AUTO-GENERATED — do not edit. Edit ~/.config/theme/colors.sh and run sync-theme.

# fzf colors
export FZF_DEFAULT_OPTS="
  --color=bg+:{{SELECTION_BG}},bg:{{BG}},spinner:{{ACCENT}},hl:{{COLOR1}}
  --color=fg:{{FG}},header:{{MUTED}},info:{{ACCENT}},pointer:{{ACCENT}}
  --color=marker:{{ACCENT}},fg+:{{FG}},prompt:{{ACCENT}},hl+:{{COLOR1}}
  --color=border:{{MUTED}}
  --border=sharp
  --prompt='  '
  --pointer='▶'
  --marker='✓'
"

# bat theme (uses built-in that best matches; sync-theme writes a custom one)
export BAT_THEME="custom"
