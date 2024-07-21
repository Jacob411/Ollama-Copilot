
local lspconfig = require 'lspconfig'
local capabilities = require('cmp_nvim_lsp').default_capabilities()
local ghost_text = require 'OllamaCopilot.ghost_text'
local ollama_client = require 'OllamaCopilot.lsp_client'
local configs = require 'lspconfig.configs'

local M = {}

-- Default configuration
local default_config = {
    model_name = "deepseek-coder:base",
    stream_suggestion = false,
    python_command = "python3",
    filetypes = {'*'},
    ollama_model_opts = {
        num_predict = 40,
        temperature = 0.1,
        stop = {'\n'}
    },
    keymaps = {
        suggestion = '<leader>os',
        accept = '<leader>oa',
        reject = '<leader>or',
        insert_accept = '<C-a>',
    },
}

-- Merge user config with default config
local function merge_config(user_config)
    if user_config then
        for k, v in pairs(user_config) do
            if type(v) == "table" then
                if default_config[k] == nil then
                    default_config[k] = v
                else
                    for key, val in pairs(v) do
                        default_config[k][key] = val
                    end
                end
            else
                default_config[k] = v
            end
        end
    end
    return default_config
end

function M.setup(user_config)
    local config = merge_config(user_config)

    if not configs.ollama_lsp then
        configs.ollama_lsp = {
            default_config = {
                cmd = {config.python_command, "python/ollama_lsp.py"},
                filetypes = config.filetypes,
                root_dir = function(fname)
                    return lspconfig.util.find_git_ancestor(fname)
                end,
                settings = {},
                init_options = {
                    model_name = config.model_name,
                    stream_suggestion = config.stream_suggestion,
                    ollama_model_opts = config.ollama_model_opts,
                },
            },
        }
    end

    lspconfig.ollama_lsp.setup{
        capabilities = capabilities,
        on_attach = function(_, bufnr)
            vim.api.nvim_create_user_command("OllamaSuggestion", ollama_client.request_completions, {desc = "Get Ollama Suggestion"})
            vim.api.nvim_create_user_command("OllamaAccept", ghost_text.accept_first_extmark_lines, {desc = "Accepts displayed Ollama Suggestion"})
            vim.api.nvim_create_user_command("OllamaReject", ghost_text.delete_first_extmark, {desc = "Rejects displayed Ollama Suggestion"})
        end,
        handlers = {
            ["textDocument/completion"] = function(err, result, ctx, config)
                local line = ctx['params']['position']['line']
                local col = ctx['params']['position']['character']
            end,
            ['$/tokenStream'] = function(err, result, ctx, config)
                local opts = ghost_text.build_opts_from_text(result['completion']['total'])
                ghost_text.add_extmark(result['line'], result['character'], opts)
            end,
        }
    }

    -- Set keymaps
    vim.api.nvim_set_keymap('n', config.keymaps.suggestion, '<Cmd>OllamaSuggestion<CR>', { noremap = true })
    vim.api.nvim_set_keymap('n', config.keymaps.accept, '<Cmd>OllamaAccept<CR>', { noremap = true })
    vim.api.nvim_set_keymap('n', config.keymaps.reject, '<Cmd>OllamaReject<CR>', { noremap = true })
    vim.api.nvim_set_keymap('i', config.keymaps.insert_accept, '<Esc>:OllamaAccept<CR>a', {noremap = true, silent = true})
end

return M

