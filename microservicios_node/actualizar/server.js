require("dotenv").config();
const express = require("express");
const axios = require("axios");
const swaggerUi = require("swagger-ui-express");

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3002;
const DJANGO_BASE_URL = (process.env.DJANGO_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");
const TOKEN = process.env.INTERNAL_API_TOKEN || "dev-internal-token";

const openapi = {
  openapi: "3.0.3",
  info: { title: "Microservicio de Actualización y Consulta", version: "1.0.0" },
  paths: {
    "/health": { get: { summary: "Estado del servicio", responses: { "200": { description: "OK" } } } },
    "/carros": { get: { summary: "Consulta inventario para resiliencia", responses: { "200": { description: "Inventario" } } } },
    "/carros/{id}": { put: { summary: "Actualiza un carro", parameters: [{ name: "id", in: "path", required: true, schema: { type: "integer" } }], requestBody: { required: true, content: { "application/json": { schema: { type: "object" } } } }, responses: { "200": { description: "Actualizado" } } } }
  }
};

app.use("/docs", swaggerUi.serve, swaggerUi.setup(openapi));
app.get("/openapi.json", (req, res) => res.json(openapi));
app.get("/health", (req, res) => res.json({ servicio: "actualizar", estado: "ok" }));

app.get("/carros", async (req, res) => {
  try {
    const response = await axios.get(`${DJANGO_BASE_URL}/carros/api/carros/`, { timeout: 5000 });
    res.json(response.data);
  } catch (error) {
    res.status(502).json({ error: "No se pudo consultar Django" });
  }
});

app.put("/carros/:id", async (req, res) => {
  try {
    const response = await axios.put(
      `${DJANGO_BASE_URL}/carros/api/interno/carros/${req.params.id}/actualizar/`,
      req.body,
      { headers: { "X-Internal-Token": TOKEN }, timeout: 8000 }
    );
    res.json({ microservicio: "node-actualizar",
      mensaje: "carros encontrados",
      carros: response.data.carros
    });
    
  } catch (error) {
    const status = error.response?.status || 502;
    res.status(status).json({ error: "No se pudo actualizar el carro", detalle: error.response?.data || error.message });
  }
});

app.listen(PORT, () => console.log(`MS actualizar escuchando en ${PORT}`));
