-- ~/.config/nvim/lua/plugins/theme.lua
-- AUTO-GENERATED — do not edit. Edit ~/.config/theme/colors.sh and run sync-theme.

return {
  -- Disable LazyVim's default colorscheme plugin
  { "folke/tokyonight.nvim", lazy = true, priority = 1000 },

  -- Load our custom colorscheme first, always
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "custom",
    },
  },
}
