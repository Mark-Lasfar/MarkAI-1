// frontend/swagger-config.js
module.exports = {
    dom_id: '#swagger-container',
    deepLinking: true,
    presets: [
      SwaggerUI.presets.apis,
      SwaggerUI.SwaggerUIStandalonePreset
    ],
    layout: "StandaloneLayout",
    defaultModelsExpandDepth: -1,
    docExpansion: 'none',
    supportedSubmitMethods: ['get', 'post', 'put', 'delete'],
    validatorUrl: null
  }