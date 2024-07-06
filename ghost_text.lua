-- demo.lua
vim.cmd [[highlight MySuggestion guifg=#757575 ctermfg=8]]

local bnr = vim.fn.bufnr('%')
ns_id = vim.api.nvim_create_namespace('demo')

local line_num = 1
local col_num = 0

local opts = {
  id = 1,
  virt_text = {{"-- Here's the first line, should be placed", "MySuggestion"}},
  virt_lines = {
    {{"-- Here's come virtual text adding in", "MySuggestion"}},
    {{"-- SECOND LINE", "MySuggestion"}}
  },
  virt_text_pos = 'inline',
  -- virt_text_win_col = 20,
}



function add_extmark()
  local cursor = vim.api.nvim_win_get_cursor(0)
  line_num = cursor[1]
  col_num = cursor[2]
  mark_id = vim.api.nvim_buf_set_extmark(0, ns_id, line_num - 1, col_num, opts)
end

function delete_first_extmark()
  vim.api.nvim_buf_del_extmark(0, ns_id, 1)
end

function get_first_extmark_text()
  local data = vim.api.nvim_buf_get_extmark_by_id(0, ns_id, mark_id, { details = true })
  local text = data[3]['virt_text'][1][1]
  for i, line in ipairs(data[3]['virt_lines']) do
    print(vim.inspect(line[1][1]))
    text = text .. "\n" .. line[1][1]
  end
  return text
end

function get_first_extmark_lines()
  local data = vim.api.nvim_buf_get_extmark_by_id(0, ns_id, mark_id, { details = true })
  print(vim.inspect(data))
  local text = data[3]['virt_text'][1][1]
  local lines = {}
  lines[#lines + 1] = text
  for i, line in ipairs(data[3]['virt_lines']) do
    table.insert(lines, line[1][1])
  end
  return {lines, data[1], data[2]} 
end

function paste_first_extmark()
  local text = get_first_extmark_text()
  delete_first_extmark()
  vim.api.nvim_paste(text, true, -1)
end

function accept_first_extmark_lines()
  local data = get_first_extmark_lines()
  local lines = data[1]
  local row = data[2]
  local col = data[3]
  delete_first_extmark()
  vim.api.nvim_buf_set_text(0, row, col, row, col, lines)
end
-- Here's the first line, should be placed
-- Here's come virtual text adding in
-- SECOND LINE -- first -- first
-- vim.api.nvim_buf_set_text(0,61, 0, 61, 0, {" -- first"}) 

vim.api.nvim_set_keymap('n', '<leader>od', '<cmd>lua delete_first_extmark()<CR>', { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>oa', '<cmd>lua add_extmark()<CR>', { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>op', '<cmd>lua accept_first_extmark_lines(66, 0)<CR>', { noremap = true, silent = true })




return {
  add_extmark = add_extmark,
}
