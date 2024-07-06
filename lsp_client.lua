
local id_2 = vim.lsp.get_clients()[1]['name'] -- Replace with your client ID
print(vim.inspect(id_2))

local lsp_client = vim.lsp.get_client_by_id(id_2)

local cursor = vim.api.nvim_win_get_cursor(0)
local position = {line = cursor[1], character = cursor[2]} -- Convert to zero-based indexing


local text_doc = vim.api.nvim_buf_get_name(0) -- Get current buffer information
print(vim.inspect(text_doc))

local function get_completions()
  local text_doc = {uri = vim.api.nvim_get_current_buf().uri} -- Get current buffer information
  local position = {line = vim.api.nvim_line() - 1, character = vim.api.nvim_col() - 1} -- Convert to zero-based indexing
  local params = {
    textDocument = text_doc,
    position = position,
  }

  local completions = lsp_client.request('textDocument/completion', params)
  print(vim.inspect(completions))
  -- Process and insert completions (see next step)
end

-- Bind the completion function to a keymap (optional)
vim.api.nvim_set_keymap('n', '<leader>cc', '<cmd>lua get_completions()<CR>', { noremap = true })
