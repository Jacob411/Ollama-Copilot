
local lspconfig = require 'lspconfig'
local capabilities = require('cmp_nvim_lsp').default_capabilities()
local ghost_text = require 'OllamaCopilot.ghost_text'
local ollama_client = require 'OllamaCopilot.lsp_client'
local configs = require 'lspconfig.configs'


local M = {}

-- TODO : add demo gif which shows tabbing the completion
-- TODO : smoother experience (no flickering) (need to not block the main thread with completion, or add client side logic to handle changes)
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



local enabled = true

local function disable_plugin()
    if not enabled then return end

    local clients = vim.lsp.get_active_clients()

    for _, client in ipairs(clients) do
        if client.name == 'ollama_lsp' then
            client.stop()
        end
    end
    -- Remove key mappings
    -- vim.api.nvim_del_keymap('n', '<leader>os')
    -- vim.api.nvim_del_keymap('n', '<leader>oa')
    -- vim.api.nvim_del_keymap('n', '<leader>or')
    -- vim.api.nvim_del_keymap('i', '<C-a>')
    --
    -- Set the enabled flag to false
    enabled = false
end

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
    local cur_file = debug.getinfo(1, 'S').source
    -- strip the leading '@' and lua/OllamaCopilot/start_up.lua from the end

    cur_file = cur_file:sub(2, -1):sub(1, -31)

    print(cur_file)
    local config = merge_config(user_config)

    if not configs.ollama_lsp then
        configs.ollama_lsp = {
            default_config = {
                cmd = {config.python_command, cur_file .. "python/ollama_lsp.py"},
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
                local cursor_line, cursor_col = unpack(vim.api.nvim_win_get_cursor(0))

                if cursor_line == result['line'] and cursor_col == result['character'] then
                    ghost_text.add_extmark(result['line'], result['character'], opts)
                elseif result['completion']['total'] == '' then
                    ghost_text.delete_first_extmark()
                end
            end,
            ['$/clearSuggestion'] = function(err, result, ctx, config)
                ghost_text.delete_first_extmark()
            end
        }
    }

    



    vim.api.nvim_command('augroup OllamaCopilot')
    -- TODO: Add autocommands to clear extmarks on insert mode and change buffer

    vim.api.nvim_create_user_command("DisableOllamaCopilot", function() disable_plugin() end, {desc = "Disables Ollama Copilot"})

    -- Set keymaps
    vim.api.nvim_set_keymap('n', config.keymaps.suggestion, '<Cmd>OllamaSuggestion<CR>', { noremap = true })
    vim.api.nvim_set_keymap('n', config.keymaps.accept, '<Cmd>OllamaAccept<CR>', { noremap = true })
    vim.api.nvim_set_keymap('n', config.keymaps.reject, '<Cmd>OllamaReject<CR>', { noremap = true })
    vim.api.nvim_set_keymap('i', config.keymaps.insert_accept, '<Esc>:OllamaAccept<CR>$a', {noremap = true, silent = true})


    vim.api.nvim_command('augroup END')
    -- def function for the tab_complete
    --
    function tab_complete()
      if ghost_text.is_visible() then
        ghost_text.accept_first_extmark_lines()
      else
        vim.api.nvim_input("<Tab>")
      end
    end

    vim.api.nvim_set_keymap("i", "<C-a>", "v:lua.tab_complete()",{expr = true, noremap = true})
    
end


return M

