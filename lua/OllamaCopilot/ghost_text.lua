
vim.cmd [[highlight MySuggestion guifg=#757575 ctermfg=8]]
ns_id = vim.api.nvim_create_namespace('demo')



function build_opts_from_text(text)
  if not text then
    return nil
  end
  -- split lines if there are multiple lines
  local lines = vim.split(text, "\n")
  local virt_lines = {}
  if #lines > 1 then
      for i = 2, #lines do
          table.insert(virt_lines, { { lines[i], "MySuggestion" } })
      end
  end
  local virt_text = { { lines[1], "MySuggestion" } }
  return {
    id = 1,
    virt_text = virt_text,
    virt_lines = virt_lines,
    virt_text_pos = 'inline',
  }
end

function add_extmark(row, col, new_opts)
  if not new_opts then
    return nil
  end
  local success, err = pcall(vim.api.nvim_buf_set_extmark, 0, ns_id, row - 1, col, new_opts)
  -- if err and col == 1 then we set to 0 and try again
  if not success and col == 1 then
    success, err = pcall(vim.api.nvim_buf_set_extmark, 0, ns_id, row - 1, 0, new_opts)
  end
end

function delete_first_extmark()
  vim.api.nvim_buf_del_extmark(0, ns_id, 1)
end

function get_first_extmark_text()
  local data = vim.api.nvim_buf_get_extmark_by_id(0, ns_id, mark_id, { details = true })
  local text = data[3]['virt_text'][1][1]
  for i, line in ipairs(data[3]['virt_lines']) do
    text = text .. "\n" .. line[1][1]
  end
  return text
end

function get_first_extmark_lines()
  local data = vim.api.nvim_buf_get_extmark_by_id(0, ns_id, 1, { details = true })
  local text = data[3]['virt_text'][1][1]
  local lines = {}

  lines[#lines + 1] = text
  if not data[3]['virt_lines'] then
    return {lines, data[1], data[2]}
  end
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
  -- return the end position of the text that was inserted
  -- this is used to move the cursor to the end of the inserted text
  return {row + #lines, col + #lines[#lines]}
end

function is_visible()
  -- checks to see if the ghost text is visible
  -- if it is, return true
  local data = vim.api.nvim_buf_get_extmark_by_id(0, ns_id, 1, { details = true })
  if not data then
    return false
  end
  if next(data) == nil then
    return false
  end
  return true
end 


return {
  add_extmark = add_extmark,
  build_opts_from_text = build_opts_from_text,
  accept_first_extmark_lines = accept_first_extmark_lines,
  delete_first_extmark = delete_first_extmark,
  is_visible = is_visible,
}
