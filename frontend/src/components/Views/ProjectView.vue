<script setup>
import ExtendedMenu from "@/components/ExtendedMenu.vue";
import { ref, onMounted, nextTick, watch } from "vue";
import Tree from 'primevue/tree';
import Button from 'primevue/button';
import ScrollPanel from 'primevue/scrollpanel';
import Tag from 'primevue/tag';
import Textarea from 'primevue/textarea';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Message from 'primevue/message';
import Toast from 'primevue/toast';
import Avatar from 'primevue/avatar';
import Skeleton from 'primevue/skeleton';
import { useToast } from 'primevue/usetoast';

const toast = useToast();
const props = defineProps({ id: [Number, String] });
const db_type = ref('')

const scrollPanelRef = ref(null);

const scrollToBottom = async () => {
  await nextTick();
  // PrimeVue ScrollPanel puts content inside a div with this class
  const scrollElement = scrollPanelRef.value?.$el.querySelector('.p-scrollpanel-content');

  if (scrollElement) {
    scrollElement.scrollTo({
      top: scrollElement.scrollHeight,
      behavior: 'smooth' // Smooth scrolling for better UX
    });
  }
};

// --- Logic ---
const schemaNodes = ref([]);
const expandedKeys = ref({});
const chatHistory = ref([]);
const userQuery = ref('');
const loading = ref(false);
const db_maps = (db) => {
  if (db === "postgres" || db === "postgresql") {
    return "PostgreSQL"
  } else if (db === "mysql") {
    return "MySQL"
  }
  else {
    return "SQL"
  }
}
const getSchema = async () => {
  try {
    const response = await fetch(`/api/projects/${props.id}/schema`);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const values = await response.json();
    schemaNodes.value = values.schema
    db_type.value = values.database_type;
    expandedKeys.value = { ...expandedKeys.value, '0': true };
  } catch (error) {
    console.error('Failed to fetch schema:', error);
  }
};

const sendMessage = async () => {
  const text = userQuery.value.trim();
  if (!text) return;

  // 1. Add user message to local UI
  const newUserMsg = {
    id: Date.now(),
    role: 'user',
    content: text,
    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  };
  chatHistory.value.push(newUserMsg);

  // 2. Prepare Context (Last 5 messages)
  // We take the history BEFORE the new message was pushed, or including it.
  // Usually, you send the previous history + the current question.
  const context = chatHistory.value
      .slice(-6) // Take last 6 (the 5 previous + the 1 we just added)
      .map(msg => ({
        role: msg.role,
        content: msg.content
      }));

  userQuery.value = '';
  loading.value = true;
  scrollToBottom();

  try {
    const response = await fetch(`/api/projects/${props.id}/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      // 3. Send the history array instead of just a string
      body: JSON.stringify({
        question: text,
        history: context
      })
    });

    if (!response.ok) throw new Error(`Server error: ${response.status}`);
    const data = await response.json();

    chatHistory.value.push({
      id: Date.now() + 1,
      role: 'assistant',
      content: data.sql ? "Here is the SQL query generated based on your request:" : data.answer || "I couldn't generate SQL.",
      sql: data.sql || null,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      results: null, isRunning: false, runError: null, columns: []
    });

  } catch (error) {
    // ... error handling
  } finally {
    loading.value = false;
    scrollToBottom();
  }
};

const runQuery = async (message) => {
  if (!message.sql) return;
  message.isRunning = true;
  message.runError = null;
  message.results = null;
  message.columns = [];

  try {
    const response = await fetch(`/api/projects/${props.id}/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sql: message.sql })
    });

    if (!response.ok) {
       const errData = await response.json().catch(() => ({}));
       throw new Error(errData.detail || `Execution failed: ${response.status}`);
    }

    const jsonResponse = await response.json();
    message.results = jsonResponse.data;
    message.columns = jsonResponse.columns;

    if (message.results.length === 0) {
      toast.add({ severity: 'info', summary: 'Executed', detail: 'Query returned 0 rows.', life: 3000 });
    } else {
      toast.add({ severity: 'success', summary: 'Success', detail: 'Query executed successfully!', life: 3000 });
    }

    await nextTick();
    scrollToBottom();

  } catch (error) {
    message.runError = error.message;
  } finally {
    message.isRunning = false;
  }
};

const getHistory = async () => {
  try {
    const response = await fetch(`/api/projects/${props.id}/history`);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const historyData = await response.json();

    // Map the database rows to the chat history format
    const formattedHistory = [];
    historyData.forEach(item => {
      // 1. Add the User's question
      formattedHistory.push({
        id: `old-u-${item.id}`,
        role: 'user',
        content: item.question,
        timestamp: new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      });

      // 2. Add the Assistant's SQL response
      formattedHistory.push({
        id: `old-a-${item.id}`,
        role: 'assistant',
        content: "Here is the SQL query generated based on your request:",
        sql: item.generated_sql,
        timestamp: new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        results: null,
        isRunning: false,
        runError: null,
        columns: []
      });
    });

    chatHistory.value = formattedHistory;

    // Scroll to the bottom after loading history
    await nextTick();
    scrollToBottom();
  } catch (error) {
    console.error('Failed to fetch history:', error);
    toast.add({ severity: 'warn', summary: 'History', detail: 'Could not load previous chat history.', life: 3000 });
  }
};
watch(chatHistory, () => {
  scrollToBottom();
}, { deep: true })
// Update onMounted to run both
onMounted(() => {
  getSchema();
  getHistory();
});

const copySQL = (sql) => {
  navigator.clipboard.writeText(sql);
  toast.add({ severity: 'success', summary: 'Copied', detail: 'SQL copied to clipboard', life: 2000 });
};
</script>

<template>
  <Toast />
  <div class="layout-wrapper">
    <ExtendedMenu class="fixed-header"/>

    <div class="workspace-container">

      <aside class="schema-panel">
        <div class="panel-header">
          <div class="flex align-items-center gap-2">
            <i class="pi pi-database text-primary text-xl"></i>
            <span class="font-bold text-lg">Explorer</span>
          </div>
          <Tag :value="db_maps(db_type)" severity="info"></Tag>
        </div>

        <div class="tree-wrapper custom-scrollbar">
          <div v-if="schemaNodes.length === 0" class="p-4">
             <Skeleton width="100%" height="2rem" class="mb-2"></Skeleton>
             <Skeleton width="80%" height="2rem" class="mb-2"></Skeleton>
          </div>
          <Tree
            v-else
            :value="schemaNodes"
            v-model:expandedKeys="expandedKeys"
            class="w-full border-none bg-transparent p-0"
            selectionMode="single"
          >
            <template #default="slotProps">
              <span class="text-sm">{{ slotProps.node.label }}</span>
            </template>
          </Tree>
        </div>
      </aside>

      <main class="chat-panel">
        <ScrollPanel ref="scrollPanelRef" class="messages-area custom-scrollbar" style="height: 100%">
          <div class="messages-container">
            <div v-if="chatHistory.length === 0 && !loading" class="text-center p-5 text-500">
              <i class="pi pi-comments text-4xl mb-3"></i>
              <p>No previous conversation. Start by asking a question!</p>
            </div>
            <div v-for="msg in chatHistory" :key="msg.id" class="message-row fade-in" :class="msg.role">

              <div class="message-content-wrapper">

                <Avatar
                  :icon="msg.role === 'assistant' ? 'pi pi-bolt' : 'pi pi-user'"
                  class="flex-shrink-0"
                  :class="msg.role === 'assistant' ? 'ai-avatar' : 'user-avatar'"
                  shape="circle"
                />

                <div class="bubble-container">
                  <div class="bubble-header">
                    <span class="font-bold text-sm">{{ msg.role === 'assistant' ? 'SQL Helper' : 'You' }}</span>
                    <span class="text-xs text-500" style="margin-left: 0.75rem;">{{ msg.timestamp }}</span>
                  </div>

                  <div class="bubble-body">
                    {{ msg.content }}
                  </div>

                  <div v-if="msg.sql" class="sql-card mt-3">
                    <div class="sql-header">
                      <div class="flex align-items-center gap-2">
                        <span class="text-primary font-bold">&lt; &gt;</span>
                        <span class="text-xs font-bold text-500">GENERATED SQL</span>
                      </div>
                      <Button
                        icon="pi pi-copy"
                        text rounded
                        size="small"
                        class="p-0 w-2rem h-2rem text-500"
                        @click="copySQL(msg.sql)"
                      />
                    </div>
                    <div class="sql-code-bg">
                      <pre><code>{{ msg.sql }}</code></pre>
                    </div>
                    <div class="sql-footer">
                       <Button
                          label="Run Query"
                          icon="pi pi-play"
                          size="small"
                          severity="success"
                          :loading="msg.isRunning"
                          @click="runQuery(msg)"
                          outlined
                        />
                    </div>
                  </div>

                  <Message v-if="msg.runError" severity="error" class="mt-2 text-xs" :closable="false">
                    {{ msg.runError }}
                  </Message>

                  <div v-if="msg.columns && msg.columns.length > 0" class="results-wrapper mt-3">
                     <div class="flex align-items-center mb-2">
                        <span class="text-lg font-bold">Results ({{ msg.results ? msg.results.length : 0 }})</span>
                     </div>
                     <DataTable
                        :value="msg.results"
                        size="small"
                        stripedRows
                        paginator :rows="5"
                        class="p-datatable-sm text-sm border-1 surface-border border-round overflow-hidden"
                        tableStyle="min-width: 100%"
                        scrollable
                      >
                        <Column v-for="col in msg.columns" :key="col" :field="col" :header="col" sortable></Column>
                      </DataTable>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="loading" class="message-row assistant fade-in">
               <div class="message-content-wrapper">
                 <Avatar icon="pi pi-spin pi-spinner" class="ai-avatar flex-shrink-0" shape="circle" />
                 <div class="bubble-container">
                   <div class="bubble-body text-500 text-sm flex align-items-center gap-2">
                     Generating SQL...
                   </div>
                 </div>
               </div>
            </div>
          </div>
        </ScrollPanel>

        <div class="input-area-wrapper">
          <div class="input-island">
             <Textarea
                v-model="userQuery"
                rows="1"
                autoResize
                placeholder="Ask your data a question..."
                class="chat-input text-base"
                @keydown.enter.prevent="sendMessage"
              />
             <Button
                icon="pi pi-send"
                text rounded
                @click="sendMessage"
                :disabled="loading || !userQuery.trim()"
                class="send-btn"
              />
          </div>
        </div>

      </main>
    </div>
  </div>
</template>

<style scoped>
/* --- Layout --- */
.layout-wrapper {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--surface-ground);
  color: var(--text-color);
}

.workspace-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* --- Schema Sidebar --- */
.schema-panel {
  width: 280px;
  background-color: var(--surface-card);
  border-right: 1px solid var(--surface-border);
  display: flex;
  flex-direction: column;
}

.panel-header {
  padding: 1.25rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--surface-border);
}

.tree-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

/* --- Chat Area --- */
.chat-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%; /* Ensure it takes full available height */
  min-height: 0; /* Crucial for flex children to allow scrolling */
  overflow: hidden; /* Prevents the whole panel from scrolling */
}

.messages-area {
  flex: 1; /* This tells the messages to take all space NOT used by the input */
  min-height: 0; /* Allows the ScrollPanel to be smaller than its content */
}
.messages-container {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 2rem; /* Increased spacing between messages */
}

.message-row {
  display: flex;
  width: 100%;
}

.message-content-wrapper {
  display: flex;
  gap: 1rem;
  max-width: 90%;
}

/* User Alignment: Right */
.message-row.user {
  justify-content: flex-end;
}
.message-row.user .message-content-wrapper {
  flex-direction: row-reverse;
}

/* Avatar Styling */
.ai-avatar {
    background-color: transparent !important;
    color: var(--text-color) !important;
}
.user-avatar {
    background-color: transparent !important;
    color: var(--text-color) !important;
}

/* Bubble Styling - Minimalist (No background for text bubbles per screenshot) */
.bubble-container {
  min-width: 200px;
  max-width: 100%;
  background: #393851;
  padding: 12px;
  border-radius: 20px;
}

.bubble-header {
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
}

/* Align user header to right */
.message-row.user .bubble-header {
  justify-content: flex-end; /* Puts name/time on right side */
  flex-direction: row-reverse; /* Puts name after time if needed, or keep standard */
}
/* IMPORTANT: Fix logic for user header alignment to match screenshot 'You 00:00' */
.message-row.user .bubble-header span:last-child {
    margin-left: 0;
    margin-right: 0.75rem; /* Margin for timestamp when reversed */
}

.bubble-body {
  line-height: 1.6;
  font-size: 1rem;
  white-space: pre-wrap;
}

/* Align user text to right */
.message-row.user .bubble-body {
    text-align: right;
}

/* --- SQL Card --- */
.sql-card {
  border: 1px solid var(--surface-border);
  border-radius: 8px;
  overflow: hidden;
  background: #202023;
  margin-top: 1rem;
  text-align: left; /* Ensure code block is always left aligned */
}

.sql-header {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--surface-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #030215
}

.sql-code-bg {
  background: #18181b; /* Deep dark for code contrast */
  padding: 1.25rem;
  overflow-x: auto;
}

.sql-code-bg pre {
  margin: 0;
  color: #e4e4e7;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 0.9rem;
}

.sql-footer {
  padding: 1rem;
  background: var(--surface-ground); /* Slightly lighter/darker than card */
}

/* --- Input Island --- */
.input-area-wrapper {
  padding: 1em;
}

.input-island {
  max-width: 900px;
  margin: 0 auto;
  padding: 0.5rem 0.5rem 0.5rem 1rem;
  display: flex;
  align-items: center;
  border: 1px solid var(--surface-border);
  border-radius: 20px;
  background: #393851;
}
.input-area-wrapper {
  flex-shrink: 0; /* Prevents the input area from being squashed */
  padding: 1rem;
  background-color: var(--surface-card); /* Optional: different bg to distinguish */
  border-top: 1px solid var(--surface-border);
}
.chat-input {
  flex: 1;
  border: none !important;
  box-shadow: none !important;
  background: transparent;
  padding: 0.75rem 0;
}

.send-btn {
  color: var(--text-color-secondary);
}

/* Animation */
.fade-in {
  animation: fadeIn 0.3s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: var(--surface-600);
  border-radius: 3px;
}
</style>