-- demo.lua
vim.cmd [[highlight MySuggestion guifg=#757575 ctermfg=8]]

local bnr = vim.fn.bufnr('%')
ns_id = vim.api.nvim_create_namespace('demo')

local line_num = 1
local col_num = 0

local opts = {
  end_line = 10,
  id = 1,
  virt_text = {{"Here's the first line, should be placed", "MySuggestion"}},
  virt_lines = {
    {{"Here's come virtual text adding in", "MySuggestion"}},
    {{"SECOND LINE", "IncSearch"}}
  },
  virt_text_pos = 'inline',
  -- virt_text_win_col = 20,
}
function add_extmark()
  local cursor = vim.api.nvim_win_get_cursor(0)
  line_num = cursor[1]
  col_num = cursor[2]
  print(line_num, col_num)
  mark_id = vim.api.nvim_buf_set_extmark(0, ns_id, line_num - 1, col_num, opts)
end

function delete_extmark()
  vim.api.nvim_buf_del_extmark(0, ns_id, 1)
end

function paste_extmark()
  local data = vim.api.nvim_buf_get_extmark_by_id(0, ns_id, mark_id, { details = true })
  local text = data[3]['virt_text'][1][1]
  print(text)

  if data then
    vim.api.put({{data[3]['virt_text'][1][1]}}, "", true, true)
  end
  --vim.api.nvim_paste(data, true, -1)
end

vim.api.nvim_set_keymap('n', '<leader>dm', '<cmd>lua delete_extmark()<CR>', { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>da', '<cmd>lua add_extmark()<CR>', { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>dp', '<cmd>lua paste_extmark()<CR>', { noremap = true, silent = true })
