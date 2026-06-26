# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
fastfetch
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

source /usr/share/cachyos-zsh-config/cachyos-config.zsh
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

plugins=(git zsh-navigation-tools)


# Enable advanced tab completion menu
autoload -Uz compinit && compinit
zstyle ':completion:*' menu select
# Tell the autosuggest plugin to look at history first, then fallback to tab-completion
export ZSH_AUTOSUGGEST_STRATEGY=(history completion)
export PATH="$HOME/.local/bin:$PATH"
alias dotfiles-sync='~/dotfiles/sync.sh'
alias dotfiles-sync='~/dotfiles/sync.sh'
alias sync-theme='~/.config/theme/sync-theme'
