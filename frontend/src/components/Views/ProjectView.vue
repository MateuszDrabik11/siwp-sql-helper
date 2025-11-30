<script setup>
import ExtendedMenu from "@/components/ExtendedMenu.vue";
import { ref, onMounted } from "vue";
import Tree from 'primevue/tree';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import ScrollPanel from 'primevue/scrollpanel';
import Tag from 'primevue/tag';
import Textarea from 'primevue/textarea';

const props = defineProps({
  id: [Number, String],
});

// --- Mock Data: Database Schema ---
// PrimeVue Tree requires specific structure: key, label, icon, children
const schemaNodes = ref([
  {
    key: '0',
    label: 'public',
    icon: 'pi pi-database',
    children: [
      {
        key: '0-0',
        label: 'users',
        icon: 'pi pi-table',
        children: [
          { key: '0-0-0', label: 'id (int8)', icon: 'pi pi-key', selectable: false },
          { key: '0-0-1', label: 'email (varchar)', icon: 'pi pi-hashtag', selectable: false },
          { key: '0-0-2', label: 'signup_date (timestamp)', icon: 'pi pi-calendar', selectable: false },
          { key: '0-0-3', label: 'status (varchar)', icon: 'pi pi-tag', selectable: false },
        ]
      },
      {
        key: '0-1',
        label: 'orders',
        icon: 'pi pi-table',
        children: [
          { key: '0-1-0', label: 'id (int8)', icon: 'pi pi-key', selectable: false },
          { key: '0-1-1', label: 'user_id (int8)', icon: 'pi pi-link', selectable: false },
          { key: '0-1-2', label: 'total_amount (numeric)', icon: 'pi pi-dollar', selectable: false },
        ]
      }
    ]
  }
]);

// --- Mock Data: Chat History ---
const chatHistory = ref([
  {
    id: 1,
    role: 'user',
    content: 'Show me the top 5 users who spent the most money last month.',
    timestamp: '10:05 AM'
  },
  {
    id: 2,
    role: 'assistant',
    content: 'Here is the query to fetch top spenders based on the `orders` table.',
    sql: `SELECT u.email, SUM(o.total_amount) as total_spent
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.created_at >= NOW() - INTERVAL '1 month'
GROUP BY u.email
ORDER BY total_spent DESC
LIMIT 5;`,
    timestamp: '10:05 AM'
  },
  {
    id: 3,
    role: 'user',
    content: 'Can you filter that for only active users?',
    timestamp: '10:06 AM'
  }
]);

const userQuery = ref('');
const loading = ref(false);

const sendMessage = () => {
  if (!userQuery.value.trim()) return;

  // Add user message
  chatHistory.value.push({
    id: Date.now(),
    role: 'user',
    content: userQuery.value,
    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  });

  loading.value = true;
  const tempQuery = userQuery.value;
  userQuery.value = '';

  // Simulate AI Response delay
  setTimeout(() => {
    chatHistory.value.push({
      id: Date.now() + 1,
      role: 'assistant',
      content: `I've updated the query to filter by status='active'.`,
      sql: `SELECT u.email, SUM(o.total_amount) as total_spent
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.created_at >= NOW() - INTERVAL '1 month'
  AND u.status = 'active' -- Added filter
GROUP BY u.email
ORDER BY total_spent DESC
LIMIT 5;`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    });
    loading.value = false;
    // Scroll to bottom logic would go here
  }, 1000);
};

// Expand all tree nodes by default
const expandedKeys = ref({ '0': true, '0-0': true, '0-1': true });
</script>

<template>
  <div class="layout-wrapper">
    <ExtendedMenu class="fixed-header"/>

    <div class="workspace-container">

      <aside class="schema-panel">
        <div class="panel-header">
          <span class="font-bold text-lg">Schema</span>
          <Tag value="PostgreSQL" severity="info"></Tag>
        </div>
        <div class="search-box">
          <span class="p-input-icon-left w-full">
            <i class="pi pi-search" />
            <InputText placeholder="Search tables..." class="w-full p-inputtext-sm" />
          </span>
        </div>
        <div class="tree-wrapper custom-scrollbar">
          <Tree
              :value="schemaNodes"
              v-model:expandedKeys="expandedKeys"
              class="w-full border-none bg-transparent"
              selectionMode="single"
          >
            <template #default="slotProps">
              <span class="text-sm">{{ slotProps.node.label }}</span>
            </template>
          </Tree>
        </div>
      </aside>

      <main class="chat-panel">

        <ScrollPanel class="messages-area custom-scrollbar">
          <div class="messages-container">
            <div v-for="msg in chatHistory" :key="msg.id" class="message-row" :class="msg.role">

              <div class="avatar-col">
                <div v-if="msg.role === 'assistant'" class="ai-avatar">
                  <i class="pi pi-bolt"></i>
                </div>
                <div v-else class="user-avatar">
                  <i class="pi pi-user"></i>
                </div>
              </div>

              <div class="content-col">
                <div class="meta">
                  <span class="role-name">{{ msg.role === 'assistant' ? 'SQL Helper' : 'You' }}</span>
                  <span class="timestamp">{{ msg.timestamp }}</span>
                </div>

                <div class="text-content">
                  {{ msg.content }}
                </div>

                <div v-if="msg.sql" class="code-block">
                  <div class="code-header">
                    <span>SQL</span>
                    <Button icon="pi pi-copy" text size="small" aria-label="Copy" />
                  </div>
                  <pre><code>{{ msg.sql }}</code></pre>
                  <div class="code-actions">
                    <Button label="Run Query" icon="pi pi-play" size="small" severity="success" outlined />
                  </div>
                </div>
              </div>

            </div>

            <div v-if="loading" class="message-row assistant">
              <div class="avatar-col"><div class="ai-avatar"><i class="pi pi-spin pi-spinner"></i></div></div>
              <div class="content-col"><span class="text-content italic">Generating SQL...</span></div>
            </div>
          </div>
        </ScrollPanel>

        <div class="input-area">
          <div class="input-wrapper">
             <Textarea
                 v-model="userQuery"
                 rows="1"
                 autoResize
                 placeholder="Ask a question about your data..."
                 class="chat-input"
                 @keydown.enter.prevent="sendMessage"
             />
            <Button icon="pi pi-send" @click="sendMessage" :disabled="loading" rounded />
          </div>
          <div class="disclaimer">AI can make mistakes. Please verify generated SQL.</div>
        </div>

      </main>

    </div>
  </div>
</template>

<style scoped>
.layout-wrapper {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--surface-ground);
}

.fixed-header {
  flex-shrink: 0;
  z-index: 100;
}

.workspace-container {
  display: flex;
  flex: 1;
  overflow: hidden; /* Important for scroll panels */
}

/* --- Schema Sidebar --- */
.schema-panel {
  width: 300px;
  background-color: var(--surface-card);
  border-right: 1px solid var(--surface-border);
  display: flex;
  flex-direction: column;
}

.panel-header {
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--surface-border);
}

.search-box {
  padding: 0.5rem 1rem;
}

.tree-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

/* --- Chat Panel --- */
.chat-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: var(--surface-ground);
  position: relative;
}

.messages-area {
  flex: 1;
  padding: 1rem;
}

.messages-container {
  max-width: 900px;
  margin: 0 auto;
  padding-bottom: 1rem;
}

.message-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  animation: fadeIn 0.3s ease;
}

.avatar-col {
  flex-shrink: 0;
}

.ai-avatar, .user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ai-avatar {
  background-color: var(--primary-color);
  color: white;
}

.user-avatar {
  background-color: var(--surface-400);
  color: white;
}

.content-col {
  flex: 1;
  min-width: 0; /* Prevents code block overflow */
}

.meta {
  margin-bottom: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.role-name {
  font-weight: 700;
  font-size: 0.9rem;
}

.timestamp {
  font-size: 0.8rem;
  color: var(--text-color-secondary);
}

.text-content {
  line-height: 1.6;
  color: var(--text-color);
}

/* --- SQL Code Block Styling --- */
.code-block {
  margin-top: 1rem;
  background-color: #1e1e1e; /* Dark theme for code */
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid var(--surface-border);
}

.code-header {
  background-color: #2d2d2d;
  color: #ccc;
  padding: 0.25rem 0.5rem;
  font-size: 0.8rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

pre {
  margin: 0;
  padding: 1rem;
  overflow-x: auto;
  color: #d4d4d4; /* VSCode light grey */
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 0.9rem;
}

.code-actions {
  padding: 0.5rem;
  background-color: #252526;
  border-top: 1px solid #333;
}

/* --- Input Area --- */
.input-area {
  padding: 1.5rem;
  background-color: var(--surface-ground);
  border-top: 1px solid var(--surface-border);
}

.input-wrapper {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  gap: 0.5rem;
  background: var(--surface-card);
  padding: 0.5rem;
  border-radius: 12px;
  border: 1px solid var(--surface-border);
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}

.chat-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 0.5rem;
  outline: none;
  resize: none;
  max-height: 100px;
}

.chat-input:focus {
  box-shadow: none;
}

.disclaimer {
  text-align: center;
  font-size: 0.75rem;
  color: var(--text-color-secondary);
  margin-top: 0.5rem;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: var(--surface-400);
  border-radius: 3px;
}
</style>