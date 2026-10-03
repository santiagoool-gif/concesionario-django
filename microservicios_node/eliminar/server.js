require("dotenv").config();
const express = require("express");
const axios = require("axios");
const swaggerUi = require("swagger-ui-express");

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3003;
const DJANGO_BASE_URL = (process.env.DJANGO_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");
const TOKEN = process.env.INTERNAL_API_TOKEN || "dev-internal-token";

const openapi = {
  openapi: "3.0.3",
  info: { title: "Microservicio de Eliminación y Respaldo", version: "1.0.0" },
  paths: {
    "/health": { get: { summary: "Estado del servicio", responses: { "200": { description: "OK" } } } },
    "/carros": { get: { summary: "Consulta inventario como respaldo", responses: { "200": { description: "Inventario" } } } },
    "/carros/{id}": { delete: { summary: "Elimina un carro", parameters: [{ name: "id", in: "path", required: true, schema: { type: "integer" } }], responses: { "200": { description: "Eliminado" } } } }
  }
};

app.use("/docs", swaggerUi.serve, swaggerUi.setup(openapi));
app.get("/openapi.json", (req, res) => res.json(openapi));
app.get("/health", (req, res) => res.json({ servicio: "eliminar", estado: "ok" }));

app.get("/carros", async (req, res) => {
  try {
    const response = await axios.get(`${DJANGO_BASE_URL}/carros/api/carros/`, { timeout: 5000 });
    res.json(response.data);
  } catch (error) {
    res.status(502).json({ error: "No se pudo consultar Django" });
  }
});

app.delete("/carros/:id", async (req, res) => {
  try {
    const response = await axios.delete(
      `${DJANGO_BASE_URL}/carros/api/interno/carros/${req.params.id}/eliminar/`,
      { headers: { "X-Internal-Token": TOKEN }, timeout: 8000 }
    );
    res.json({ microservicio: "node-eliminar", ...response.data });
  } catch (error) {
    const status = error.response?.status || 502;
    res.status(status).json({ error: "No se pudo eliminar el carro", detalle: error.response?.data || error.message });
  }
});

app.listen(PORT, () => console.log(`MS eliminar escuchando en ${PORT}`));
