require("dotenv").config();
const express = require("express");
const axios = require("axios");
const swaggerUi = require("swagger-ui-express");

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3001;
const DJANGO_BASE_URL = (process.env.DJANGO_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");
const TOKEN = process.env.INTERNAL_API_TOKEN || "dev-internal-token";

const openapi = {
  openapi: "3.0.3",
  info: { title: "Microservicio de Inserción de Carros", version: "1.0.0" },
  paths: {
    "/health": { get: { summary: "Estado del servicio", responses: { "200": { description: "OK" } } } },
    "/carros": {
      post: {
        summary: "Inserta un carro",
        requestBody: {
          required: true,
          content: { "application/json": { schema: { $ref: "#/components/schemas/CarroEntrada" } } }
        },
        responses: { "201": { description: "Creado" }, "400": { description: "Datos inválidos" }, "502": { description: "Django no disponible" } }
      }
    }
  },
  components: { schemas: { CarroEntrada: { type: "object", required: ["carro_text", "precio", "pub_date"], properties: { carro_text: { type: "string" }, precio: { type: "string" }, pub_date: { type: "string", format: "date-time" } } } } }
};

app.use("/docs", swaggerUi.serve, swaggerUi.setup(openapi));
app.get("/openapi.json", (req, res) => res.json(openapi));
app.get("/health", (req, res) => res.json({ servicio: "insertar", estado: "ok" }));

app.post("/carros", async (req, res) => {
  try {
    const response = await axios.post(
      `${DJANGO_BASE_URL}/carros/api/interno/carros/crear/`,
      req.body,
      { headers: { "X-Internal-Token": TOKEN }, timeout: 8000 }
    );
    res.status(201).json({ microservicio: "node-insertar", ...response.data });
  } catch (error) {
    const status = error.response?.status || 502;
    res.status(status).json({ error: "No se pudo insertar el carro", detalle: error.response?.data || error.message });
  }
});

app.listen(PORT, () => console.log(`MS insertar escuchando en ${PORT}`));
