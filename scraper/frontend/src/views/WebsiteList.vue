<template>
  <div class="website-list">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <h2>Website Management</h2>
          <el-button type="primary" @click="showAddWebsiteForm">
            Add Website
          </el-button>
        </div>
      </template>
      
      <!-- Websites List -->
      <el-table
        v-loading="loading"
        :data="websites"
        style="width: 100%"
        border
      >
        <el-table-column prop="name" label="Name" width="180" />
        <el-table-column prop="url" label="URL" min-width="250" show-overflow-tooltip />
        <el-table-column prop="type" label="Type" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.type === 'html' ? 'success' : 'warning'">
              {{ scope.row.type.toUpperCase() }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="Description" min-width="200" show-overflow-tooltip />
        <el-table-column prop="active" label="Status" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.active ? 'success' : 'info'">
              {{ scope.row.active ? 'Active' : 'Inactive' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="250">
          <template #default="scope">
            <el-button 
              size="small" 
              type="primary" 
              @click="editWebsite(scope.row)"
              plain
            >
              Edit
            </el-button>
            <el-button 
              size="small" 
              type="success" 
              @click="testWebsite(scope.row)"
              plain
            >
              Test
            </el-button>
            <el-button 
              size="small" 
              type="danger" 
              @click="confirmDelete(scope.row)"
              plain
            >
              Delete
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Add/Edit Website Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEditing ? 'Edit Website' : 'Add Website'"
      width="50%"
    >
      <el-form 
        :model="websiteForm" 
        :rules="formRules" 
        ref="websiteFormRef" 
        label-width="120px"
      >
        <el-form-item label="Name" prop="name">
          <el-input v-model="websiteForm.name" placeholder="Enter website name" />
        </el-form-item>
        
        <el-form-item label="URL" prop="url">
          <el-input v-model="websiteForm.url" placeholder="Enter website URL" />
        </el-form-item>
        
        <el-form-item label="Description" prop="description">
          <el-input 
            v-model="websiteForm.description" 
            type="textarea" 
            placeholder="Enter description" 
          />
        </el-form-item>
        
        <el-form-item label="Type" prop="type">
          <el-select v-model="websiteForm.type" placeholder="Select type">
            <el-option label="HTML Scraper" value="html" />
            <el-option label="API Scraper" value="api" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="Status" prop="active">
          <el-switch 
            v-model="websiteForm.active" 
            active-text="Active" 
            inactive-text="Inactive" 
          />
        </el-form-item>

        <template v-if="websiteForm.type === 'html'">
          <el-divider content-position="left">HTML Selectors</el-divider>
          
          <el-form-item label="Main Container">
            <el-input 
              v-model="websiteForm.selectors.container" 
              placeholder="CSS Selector for main container" 
            />
          </el-form-item>
          
          <el-form-item label="Item Selector">
            <el-input 
              v-model="websiteForm.selectors.item" 
              placeholder="CSS Selector for each item" 
            />
          </el-form-item>
          
          <el-form-item label="Title Selector">
            <el-input 
              v-model="websiteForm.selectors.title" 
              placeholder="CSS Selector for title" 
            />
          </el-form-item>
          
          <el-form-item label="Link Selector">
            <el-input 
              v-model="websiteForm.selectors.link" 
              placeholder="CSS Selector for link" 
            />
          </el-form-item>
        </template>

        <template v-if="websiteForm.type === 'api'">
          <el-divider content-position="left">API Configuration</el-divider>
          
          <el-form-item label="API Method">
            <el-select v-model="websiteForm.config.method" placeholder="Select method">
              <el-option label="GET" value="get" />
              <el-option label="POST" value="post" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="Headers">
            <el-input 
              v-model="websiteForm.config.headers" 
              type="textarea" 
              placeholder="Enter headers (JSON format)" 
            />
          </el-form-item>
          
          <el-form-item label="Request Body">
            <el-input 
              v-model="websiteForm.config.body" 
              type="textarea" 
              placeholder="Enter request body (JSON format)" 
            />
          </el-form-item>
          
          <el-form-item label="Data Path">
            <el-input 
              v-model="websiteForm.config.dataPath" 
              placeholder="JSON path to data (e.g. data.items)" 
            />
          </el-form-item>
        </template>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="saveWebsite">Save</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
  name: 'WebsiteList',
  data() {
    return {
      loading: false,
      websites: [],
      dialogVisible: false,
      isEditing: false,
      currentWebsiteId: null,
      websiteForm: {
        name: '',
        url: '',
        description: '',
        type: 'html',
        active: true,
        selectors: {
          container: '',
          item: '',
          title: '',
          link: ''
        },
        config: {
          method: 'get',
          headers: '',
          body: '',
          dataPath: ''
        }
      },
      formRules: {
        name: [
          { required: true, message: 'Please enter website name', trigger: 'blur' },
          { min: 2, max: 50, message: 'Length should be 2 to 50 characters', trigger: 'blur' }
        ],
        url: [
          { required: true, message: 'Please enter website URL', trigger: 'blur' },
          { pattern: /^https?:\/\/.+/, message: 'URL should start with http:// or https://', trigger: 'blur' }
        ],
        type: [
          { required: true, message: 'Please select website type', trigger: 'change' }
        ]
      }
    };
  },
  created() {
    this.fetchWebsites();
  },
  methods: {
    async fetchWebsites() {
      this.loading = true;
      try {
        const response = await axios.get('/api/websites');
        this.websites = response.data;
      } catch (error) {
        console.error('Error fetching websites:', error);
        ElMessage.error('Failed to load websites');
      } finally {
        this.loading = false;
      }
    },
    
    showAddWebsiteForm() {
      this.isEditing = false;
      this.currentWebsiteId = null;
      this.resetForm();
      this.dialogVisible = true;
    },
    
    editWebsite(website) {
      this.isEditing = true;
      this.currentWebsiteId = website.id;
      
      // Deep copy the website data to the form
      this.websiteForm = {
        name: website.name,
        url: website.url,
        description: website.description || '',
        type: website.type,
        active: website.active,
        selectors: { ...website.selectors } || {
          container: '',
          item: '',
          title: '',
          link: ''
        },
        config: { ...website.config } || {
          method: 'get',
          headers: '',
          body: '',
          dataPath: ''
        }
      };
      
      // Handle string JSON fields
      if (typeof this.websiteForm.config.headers === 'object') {
        this.websiteForm.config.headers = JSON.stringify(this.websiteForm.config.headers, null, 2);
      }
      
      if (typeof this.websiteForm.config.body === 'object') {
        this.websiteForm.config.body = JSON.stringify(this.websiteForm.config.body, null, 2);
      }
      
      this.dialogVisible = true;
    },
    
    async saveWebsite() {
      try {
        // Validate form
        await this.$refs.websiteFormRef.validate();
        
        // Prepare data - parse JSON strings to objects
        const websiteData = { ...this.websiteForm };
        
        if (websiteData.type === 'api') {
          try {
            if (websiteData.config.headers) {
              websiteData.config.headers = JSON.parse(websiteData.config.headers);
            }
            
            if (websiteData.config.body) {
              websiteData.config.body = JSON.parse(websiteData.config.body);
            }
          } catch (e) {
            ElMessage.error('Invalid JSON in headers or body');
            return;
          }
        }
        
        if (this.isEditing) {
          // Update existing website
          await axios.put(`/api/websites/${this.currentWebsiteId}`, websiteData);
          ElMessage.success('Website updated successfully');
        } else {
          // Create new website
          await axios.post('/api/websites', websiteData);
          ElMessage.success('Website added successfully');
        }
        
        // Close dialog and refresh list
        this.dialogVisible = false;
        this.fetchWebsites();
        
      } catch (error) {
        console.error('Error saving website:', error);
        ElMessage.error(error.response?.data?.detail || 'Failed to save website');
      }
    },
    
    confirmDelete(website) {
      ElMessageBox.confirm(
        `Are you sure you want to delete "${website.name}"?`,
        'Warning',
        {
          confirmButtonText: 'Delete',
          cancelButtonText: 'Cancel',
          type: 'warning',
        }
      )
        .then(() => {
          this.deleteWebsite(website.id);
        })
        .catch(() => {
          // User cancelled
        });
    },
    
    async deleteWebsite(id) {
      try {
        await axios.delete(`/api/websites/${id}`);
        ElMessage.success('Website deleted successfully');
        this.fetchWebsites();
      } catch (error) {
        console.error('Error deleting website:', error);
        ElMessage.error('Failed to delete website');
      }
    },
    
    async testWebsite(website) {
      try {
        ElMessage.info('Testing website connection...');
        const response = await axios.get(`/api/websites/test/${website.id}`);
        
        if (response.data.success) {
          ElMessage.success('Connection successful!');
        } else {
          ElMessage.warning(response.data.message || 'Connection test failed');
        }
      } catch (error) {
        console.error('Error testing website:', error);
        ElMessage.error('Connection test failed');
      }
    },
    
    resetForm() {
      this.websiteForm = {
        name: '',
        url: '',
        description: '',
        type: 'html',
        active: true,
        selectors: {
          container: '',
          item: '',
          title: '',
          link: ''
        },
        config: {
          method: 'get',
          headers: '',
          body: '',
          dataPath: ''
        }
      };
      
      if (this.$refs.websiteFormRef) {
        this.$refs.websiteFormRef.resetFields();
      }
    }
  }
};
</script>

<style scoped>
.website-list {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 