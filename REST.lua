
local http = require("socket.http")
local json = require("lunajson")  -- Assuming you have a JSON library

local url = "http://localhost:11434/api/generate"

local data = {
  model = "custom-deepseek",
  prompt = "import torch",
  stream = true,
  options = {
    temperature = 0.5,
    num_predict = 40,
  }
}

local request_body = json.encode(data)
local headers = {
  ["Content-Type"] = "application/json",
}


local request, err = http.request({
  url = url,
  method = "POST",
  headers = headers,
  body = request_body,
})

if err then
  print("Error sending request:", err)
else
  local response = json.decode(request)
  print(response)
end
