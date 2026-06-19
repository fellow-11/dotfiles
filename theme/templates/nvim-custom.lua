-- ~/.config/nvim/colors/custom.lua
-- AUTO-GENERATED — do not edit. Edit ~/.config/theme/colors.sh and run sync-theme.

vim.cmd("hi clear")
if vim.fn.exists("syntax_on") then vim.cmd("syntax reset") end
vim.g.colors_name = "custom"
vim.o.termguicolors = true

local c = {
    bg       = "{{BG}}",
    fg       = "{{FG}}",
    accent   = "{{ACCENT}}",
    cursor   = "{{CURSOR}}",
    muted    = "{{MUTED}}",
    sel_bg   = "{{SELECTION_BG}}",
    sel_fg   = "{{SELECTION_FG}}",
    black    = "{{COLOR0}}",
    red      = "{{COLOR1}}",
    yellow   = "{{COLOR2}}",
    orange   = "{{COLOR3}}",
    blue     = "{{COLOR4}}",
    magenta  = "{{COLOR5}}",
    white    = "{{COLOR7}}",
    br_black = "{{COLOR8}}",
    br_white = "{{COLOR15}}",
}

local function hi(group, opts)
    vim.api.nvim_set_hl(0, group, opts)
end

-- Editor chrome
hi("Normal",        { fg = c.fg,      bg = c.bg })
hi("NormalFloat",   { fg = c.fg,      bg = c.bg })
hi("LineNr",        { fg = c.muted })
hi("CursorLine",    { bg = c.black })
hi("CursorLineNr",  { fg = c.accent,  bold = true })
hi("SignColumn",    { bg = c.bg })
hi("ColorColumn",   { bg = c.black })
hi("VertSplit",     { fg = c.muted })
hi("WinSeparator",  { fg = c.muted })
hi("StatusLine",    { fg = c.fg,      bg = c.black })
hi("StatusLineNC",  { fg = c.muted,   bg = c.bg })
hi("TabLine",       { fg = c.muted,   bg = c.black })
hi("TabLineFill",   { bg = c.bg })
hi("TabLineSel",    { fg = c.accent,  bg = c.bg,    bold = true })

-- Cursor & selection
hi("Cursor",        { fg = c.bg,      bg = c.cursor })
hi("Visual",        { fg = c.sel_fg,  bg = c.sel_bg })
hi("Search",        { fg = c.bg,      bg = c.accent })
hi("IncSearch",     { fg = c.bg,      bg = c.yellow })
hi("MatchParen",    { fg = c.accent,  bold = true })

-- Syntax
hi("Comment",       { fg = c.muted,   italic = true })
hi("Constant",      { fg = c.yellow })
hi("String",        { fg = c.yellow })
hi("Number",        { fg = c.yellow })
hi("Boolean",       { fg = c.accent })
hi("Identifier",    { fg = c.fg })
hi("Function",      { fg = c.accent })
hi("Statement",     { fg = c.red })
hi("Keyword",       { fg = c.red })
hi("Operator",      { fg = c.fg })
hi("PreProc",       { fg = c.magenta })
hi("Include",       { fg = c.magenta })
hi("Type",          { fg = c.blue })
hi("Special",       { fg = c.accent })
hi("Delimiter",     { fg = c.muted })
hi("Todo",          { fg = c.bg,      bg = c.accent, bold = true })
hi("Error",         { fg = c.red,     bold = true })
hi("Warning",       { fg = c.yellow })

-- Popup menu
hi("Pmenu",         { fg = c.fg,      bg = c.black })
hi("PmenuSel",      { fg = c.bg,      bg = c.accent })
hi("PmenuSbar",     { bg = c.black })
hi("PmenuThumb",    { bg = c.muted })

-- Diagnostics
hi("DiagnosticError",   { fg = c.red })
hi("DiagnosticWarn",    { fg = c.yellow })
hi("DiagnosticInfo",    { fg = c.blue })
hi("DiagnosticHint",    { fg = c.muted })

-- Diff
hi("DiffAdd",       { fg = c.yellow,  bg = c.bg })
hi("DiffChange",    { fg = c.blue,    bg = c.bg })
hi("DiffDelete",    { fg = c.red,     bg = c.bg })
hi("DiffText",      { fg = c.accent,  bg = c.bg })

-- Treesitter (links to base groups mostly, override key ones)
hi("@keyword",          { fg = c.red })
hi("@function",         { fg = c.accent })
hi("@function.builtin", { fg = c.orange })
hi("@string",           { fg = c.yellow })
hi("@number",           { fg = c.yellow })
hi("@comment",          { fg = c.muted,  italic = true })
hi("@type",             { fg = c.blue })
hi("@variable",         { fg = c.fg })
hi("@property",         { fg = c.fg })
hi("@punctuation",      { fg = c.muted })
hi("@operator",         { fg = c.fg })
