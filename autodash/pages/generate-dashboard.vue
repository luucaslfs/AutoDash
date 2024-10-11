<template>
  <div class="bg-white min-h-screen">
    <!-- Main Content -->
    <main class="container mx-auto p-8">
      <h2 class="text-[var(--color-primary)] text-3xl font-bold mb-6">Generate Dashboard</h2>

      <!-- Upload de Arquivo -->
      <div class="flex justify-center mb-6">
        <label
          for="file-upload"
          class="btn-primary"
        >
          Upload File
          <input
            id="file-upload"
            type="file"
            class="hidden"
            @change="handleFileUpload"
            accept=".csv,.xlsx"
          />
        </label>
      </div>

      <!-- Pré-visualização dos Dados -->
      <div v-if="previewData" class="mb-6">
        <h3 class="text-2xl font-semibold mb-2 text-[var(--color-primary)]">Data Preview</h3>
        <div class="preview-container border border-gray-200 rounded-lg">
          <table class="preview-table w-full">
            <thead>
              <tr>
                <th v-for="header in previewData.columns" :key="header" class="px-4 py-2 text-left text-white-800 bg-gray-100 sticky top-0 font-semibold">
                  {{ header }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in previewData.data.slice(0, 5)" :key="index" class="hover:bg-gray-50 transition-colors duration-150 ease-in-out">
                <td v-for="(cell, cellIndex) in row" :key="cellIndex" class="px-4 py-2 border-b border-gray-200 text-gray-700">
                  {{ cell }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="mt-2 text-sm text-gray-600">
          Showing first 5 rows of {{ previewData.data.length }} total rows.
        </p>
      </div>

      <!-- Seleção do Modelo AI -->
      <div v-if="filePreview" class="mb-6">
        <label class="block mb-2 font-semibold text-[var(--color-primary)]">Select AI Model:</label>
        <select v-model="selectedModel" class="input-field">
          <option value="claude">Claude</option>
          <option value="openai">OpenAI</option>
        </select>
      </div>

      <!-- Botão para Gerar Dashboard -->
      <button
        v-if="filePreview"
        @click="generateDashboard"
        :disabled="isGenerating"
        class="btn-primary w-full"
      >
        {{ isGenerating ? "Generating..." : "Generate Dashboard" }}
      </button>

      <!-- Código Gerado e Botões -->
      <div v-if="generatedCode" class="mt-8">
        <h3 class="text-2xl font-semibold mb-2 text-gray-700">
          Generated Streamlit Dashboard Code
        </h3>
        <div class="relative">
          <pre class="bg-gray-100 p-4 rounded-lg overflow-x-auto text-gray-800">{{ generatedCode }}</pre>
          <button
            @click="copyCode"
            class="absolute top-2 right-2 btn-secondary text-sm"
          >
            Copy
          </button>
        </div>

        <div class="flex space-x-4 mt-4">
          <!-- Botão de Download do Projeto Estruturado -->
          <button
            @click="downloadZip"
            :disabled="!uniqueId || isDownloading"
            class="btn-primary flex-1"
          >
            <span v-if="isDownloading">Downloading...</span>
            <span v-else>Download Project</span>
          </button>

          <!-- Botão para Criar Repositório GitHub -->
          <button
            @click="createGitHubRepo"
            :disabled="!uniqueId || isCreatingRepo"
            class="btn-secondary flex-1"
          >
            <span v-if="isCreatingRepo">Creating Repo...</span>
            <span v-else>Create GitHub Repo</span>
          </button>
        </div>
      </div>

      <!-- Resultado da criação do repositório GitHub -->
      <div v-if="repoCreationResult" class="mt-8 bg-gray-100 shadow-md rounded-lg p-6">
        <h3 class="text-2xl font-bold mb-4 text-green-500">GitHub Repository Created</h3>
        <div class="space-y-4">
          <div>
            <span class="font-semibold text-gray-700">Result:</span>
            <span class="ml-2 text-[var(--color-secondary)]">{{ repoCreationResult.message }}</span>
          </div>
          <div>
            <span class="font-semibold text-gray-700">Repository URL:</span>
            <a :href="repoCreationResult.repo_url" target="_blank" class="ml-2 text-[var(--color-secondary)] hover:underline">
              {{ repoCreationResult.repo_url }}
            </a>
          </div>
        </div>
      </div>

      <!-- Mensagem de Erro -->
      <p v-if="error" class="error mt-4 text-red-500">{{ error }}</p>

    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRuntimeConfig } from "#app";
import Papa from "papaparse";
import { useAuthStore } from "~/stores/auth";

const config = useRuntimeConfig();
const authStore = useAuthStore();

// Estado reativo
const filePreview = ref("");
const generatedCode = ref("");
const uniqueId = ref("");
const isGenerating = ref(false);
const isDownloading = ref(false);
const isCreatingRepo = ref(false);
const previewData = ref(null);
const selectedModel = ref("claude");
const error = ref("");
const successMessage = ref("");
const repoCreationResult = ref(null);


// Handler de upload de arquivo
const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target.result;

      Papa.parse(content, {
        complete: (results) => {
          const headers = results.data[0];
          const data = results.data
            .slice(1)
            .filter((row) => row.some((cell) => cell.trim() !== ""));

          filePreview.value = results.data
            .slice(0, 6)
            .map((row) => row.join(","))
            .join("\n");
          previewData.value = { columns: headers, data: data };

          console.log("Parsed data:", previewData.value);
        },
        error: (error) => {
          console.error("Error parsing CSV:", error);
          error.value = "Error parsing CSV file. Please check the file format.";
        },
      });
    };
    reader.readAsText(file);
  }
};

// Função para gerar o dashboard
const generateDashboard = async () => {
  if (!previewData.value) return;

  isGenerating.value = true;
  error.value = "";
  successMessage.value = "";
  try {
    const requestBody = {
      table_data: previewData.value,
      model: selectedModel.value,
    };

    const response = await fetch(
      `${config.public.apiBase}/api/v1/generate-dashboard`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      }
    );

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to generate dashboard: ${errorText}`);
    }

    const result = await response.json();
    generatedCode.value = result.dashboard_code;
    uniqueId.value = result.unique_id;
    successMessage.value = "Dashboard generated successfully!";
  } catch (error) {
    console.error("Error generating dashboard:", error);
    error.value = `Failed to generate dashboard: ${error.message}`;
  } finally {
    isGenerating.value = false;
  }
};

// Função para copiar o código gerado
const copyCode = () => {
  navigator.clipboard.writeText(generatedCode.value);
  successMessage.value = "Code copied to clipboard!";
};

// Função para baixar o projeto estruturado
const downloadZip = async () => {
  if (!uniqueId.value) {
    error.value = "Unique ID not found. Please generate the dashboard first.";
    return;
  }

  isDownloading.value = true;
  error.value = "";
  successMessage.value = "";

  try {
    const requestBody = {
      unique_id: uniqueId.value,
    };

    const response = await fetch(
      `${config.public.apiBase}/api/v1/download-dashboard`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      }
    );

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to download project: ${errorText}`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'dashboard_project.zip';
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);

    successMessage.value = "Project downloaded successfully!";
    
    // Não limparemos mais o estado aqui
  } catch (error) {
    console.error("Error downloading project:", error);
    error.value = `Failed to download project: ${error.message}`;
  } finally {
    isDownloading.value = false;
  }
};

// Função para limpar o estado manualmente
const clearState = () => {
  generatedCode.value = "";
  uniqueId.value = "";
  filePreview.value = "";
  previewData.value = null;
  selectedModel.value = "claude";
  successMessage.value = "";
  error.value = "";
  repoCreationResult.value = null;
};

// Função para criar o repositório GitHub
const createGitHubRepo = async () => {
  if (!uniqueId.value || !generatedCode.value) {
    error.value = "Please generate the dashboard first.";
    return;
  }

  isCreatingRepo.value = true;
  error.value = "";
  successMessage.value = "";
  repoCreationResult.value = null;

  try {
    const repoName = `autodash-${uniqueId.value}`;
    const requestBody = {
      access_token: authStore.token,
      repo_name: repoName,
      description: "AutoDash generated Streamlit dashboard",
      table_data: previewData.value,
      generated_code: generatedCode.value
    };

    const response = await fetch(
      `${config.public.apiBase}/api/v1/create-github-repo`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      }
    );

    const result = await response.json();

    if (result.message === "GitHub App not installed") {
      console.log("Redirecting to GitHub App installation page...");
      window.location.href = result.installation_url;
      return;
    }

    if (!response.ok) {
      throw new Error(result.detail || 'Failed to create repository');
    }

    repoCreationResult.value = result;
    successMessage.value = result.message || "GitHub repository created successfully!";
  } catch (error) {
    console.error("Error creating GitHub repository:", error);
    error.value = `Failed to create GitHub repository: ${error.message}`;
  } finally {
    isCreatingRepo.value = false;
  }
};
</script>

<style scoped>
.container {
  max-width: 1000px;
}

.preview-container {
  height: 260px; /* Altura ajustada para 5 linhas */
  overflow: auto;
  border: 1px solid var(--color-primary);
  border-radius: 0.5rem;
  background-color: white;
}

.preview-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.preview-table th {
  position: sticky;
  top: 0;
  z-index: 10;
  background-color: var(--color-primary);
}

.preview-table td {
  white-space: nowrap;
  max-width: none; /* Remove a limitação de largura máxima */
}

/* Estiliza a barra de rolagem para navegadores WebKit (Chrome, Safari, etc.) */
.preview-container::-webkit-scrollbar {
  width: 12px;
  height: 12px;
}

.preview-container::-webkit-scrollbar-track {
  background: gray;
}

.preview-container::-webkit-scrollbar-thumb {
  background-color: var(--color-secondary);
  border-radius: 6px;
  border: 3px solid grey;
}

/* Estiliza a barra de rolagem para Firefox */
.preview-container {
  scrollbar-width: thin;
  scrollbar-color: var(--color-primary);
}
</style>