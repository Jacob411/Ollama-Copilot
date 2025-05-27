
local lspconfig = require 'lspconfig'
local capabilities = require('cmp_nvim_lsp').default_capabilities()
local ghost_text = require 'OllamaCopilot.ghost_text'
local ollama_client = require 'OllamaCopilot.lsp_client'
local configs = require 'lspconfig.configs'

-- TODO : update tabs and spacing to be uniform at the client side














local M = {}

-- TODO : smoother experience (no flickering) (need to not block the main thread with completion, or add client side logic to handle changes)
-- Default configuration
local default_config = {
    model_name = "deepseek-coder:base",
    stream_suggestion = false,
    python_command = "python3",
    filetypes = {'python', 'lua','vim', "markdown"},
    ollama_model_opts = {
        num_predict = 40,
        temperature = 0.1,
        --stop = {'\n'}
    },
    keymaps = {
        suggestion = '<leader>os',
        reject = '<leader>or',
        insert_accept = '<Tab>',
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
    if user_config == nil then
        user_config = {}
    end
    local cur_file = debug.getinfo(1, 'S').source
    -- strip the leading '@' and lua/OllamaCopilot/start_up.lua from the end

    print('Starting Ollama Copilot')
    cur_file = cur_file:sub(2, -1):sub(1, -31)

    local config = merge_config(user_config)

    if not configs.ollama_lsp then
        configs.ollama_lsp = {
            default_config = {
                cmd = {config.python_command, cur_file .. "python/ollama_lsp.py"},
                filetypes = config.filetypes,
                root_dir = function(fname)
                    local potential_root = lspconfig.util.find_git_ancestor(fname)
                    if potential_root then
                        return potential_root
                    else
                        return lspconfig.util.path.dirname(fname)
                    end
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
    function capture_tab_behavior()
        -- Get the existing keymap for Tab in insert mode
        local existing_tab_keymap = vim.api.nvim_get_keymap('i')
        for _, keymap in ipairs(existing_tab_keymap) do
            if keymap.lhs == '<Tab>' then
                return keymap.callback
            end
        end
        return function()
            print('No original tab behavior found')
        end
    end

    original_tab_behaviour = capture_tab_behavior()
    function tab_complete()
        local visible = ghost_text.is_visible()
        if visible then
            paste_end = ghost_text.accept_first_extmark_lines()
            local row_offset = paste_end[1]
            local col_offset = paste_end[2] + 10
            -- move cursor to the end of the line
            print(row_offset, col_offset)
            vim.api.nvim_win_set_cursor(0, { row_offset, col_offset })
        else
            original_tab_behaviour()
        end
    end


    


    
    lspconfig.ollama_lsp.setup{
        capabilities = capabilities,
        on_attach = function(_, bufnr)
            vim.api.nvim_create_user_command("OllamaSuggestion", ollama_client.request_completions, {desc = "Get Ollama Suggestion"})
            vim.api.nvim_create_user_command("OllamaAccept", ghost_text.accept_first_extmark_lines, {desc = "Accepts displayed Ollama Suggestion"})
            vim.api.nvim_create_user_command("OllamaReject", ghost_text.delete_first_extmark, {desc = "Rejects displayed Ollama Suggestion"})
            vim.keymap.set("i", config.keymaps.insert_accept,
                function()
                    tab_complete()
                end
            )
        end,
        handlers = {
            ["textDocument/completion"] = function(err, result, ctx, config)
                local line = ctx['params']['position']['line']
                local col = ctx['params']['position']['character']
            end,
            ['$/tokenStream'] = function(err, result, ctx, config)
                local opts = ghost_text.build_opts_from_text(result['completion']['total'])
                local cursor_line, cursor_col = unpack(vim.api.nvim_win_get_cursor(0))

                ghost_text.add_extmark(result['line'], result['character'], opts)
        
            end,
            ['$/clearSuggestion'] = function(err, result, ctx, config)
                ghost_text.delete_first_extmark()
            end
        }
    }


    


    vim.api.nvim_command('augroup OllamaCopilot')
    -- Auto commands
    vim.api.nvim_create_autocmd("InsertLeave", {
        pattern = "*",
        callback = function()
           ghost_text.delete_first_extmark()
        end,
    })
    -- create autocmd to delete the ghost text when the cursor moves
    vim.api.nvim_create_autocmd("CursorMoved", {
        pattern = "*",
        callback = function()
            ghost_text.delete_first_extmark()
        end,
    })

    
    



    vim.api.nvim_create_user_command("DisableOllamaCopilot", function() disable_plugin() end, {desc = "Disables Ollama Copilot"})
  
    vim.api.nvim_set_keymap('n', config.keymaps.suggestion, '<Cmd>OllamaSuggestion<CR>', { noremap = true })
    vim.api.nvim_set_keymap('n', config.keymaps.reject, '<Cmd>OllamaReject<CR>', { noremap = true })


    vim.api.nvim_command('augroup END')
    
end


return M

