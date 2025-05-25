export const endpoints = {
    getEmployeeMessages: (employeeId: string) => `/employees/${employeeId}/messages`,
    updateProductFrequency: () => '/products/frequency',
    getProductInfo: () => '/products/info',
    getStoreEmployees: (storeId: string) => `/stores/${storeId}/employees`,
    getEmployeeSchedule: (employeeId: string) => `/employees/${employeeId}/schedule`,
  };
  