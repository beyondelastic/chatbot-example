targetScope = 'subscription'

param resourceLocation string = 'westeurope'

resource rg 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  name: 'rg-aullah-chatbot'
  location: resourceLocation
}

module openai './openai.bicep' = {
  scope: rg
  name: 'openai'
  params: {
    location : resourceLocation
    openAIAccountName: 'aullah-openai'
  }
}
