'use client';

import { useState, useEffect } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Paper, 
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress,
  Alert,
  Button
} from '@mui/material';
import { artistService } from '../services/api';

// 定义表格数据类型
interface TestData {
  message: string;
  filters_applied: Record<string, any>;
  result: string;
}

export default function TablePage() {
  // 状态
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [testData, setTestData] = useState<TestData | null>(null);
  
  // 加载数据
  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // 调用测试API获取数据
      const response = await artistService.getAllTestData();
      setTestData(response);
    } catch (err) {
      setError('获取数据时发生错误');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  
  // 组件加载时获取数据
  useEffect(() => {
    fetchData();
  }, []);
  
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom>
        测试数据表格
      </Typography>
      
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'flex-end' }}>
        <Button 
          variant="contained" 
          color="primary" 
          onClick={fetchData}
          disabled={loading}
        >
          刷新数据
        </Button>
      </Box>
      
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      )}
      
      {error && (
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
      )}
      
      {testData && (
        <Paper sx={{ width: '100%', overflow: 'hidden' }}>
          <TableContainer sx={{ maxHeight: 440 }}>
            <Table stickyHeader aria-label="测试数据表格">
              <TableHead>
                <TableRow>
                  <TableCell>属性</TableCell>
                  <TableCell>值</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                <TableRow>
                  <TableCell>消息</TableCell>
                  <TableCell>{testData.message}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>应用的过滤器</TableCell>
                  <TableCell>
                    <pre>{JSON.stringify(testData.filters_applied, null, 2)}</pre>
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>结果</TableCell>
                  <TableCell>{testData.result}</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      )}
      
      <Box sx={{ mt: 4 }}>
        <Typography variant="h5" gutterBottom>
          API 响应详情
        </Typography>
        
        {testData && (
          <Paper sx={{ p: 3, bgcolor: 'background.paper' }}>
            <pre style={{ overflow: 'auto', maxHeight: '400px' }}>
              {JSON.stringify(testData, null, 2)}
            </pre>
          </Paper>
        )}
      </Box>
    </Container>
  );
} 