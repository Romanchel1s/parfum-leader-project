/* eslint-disable @typescript-eslint/no-unused-vars */
const mockApi = {
    getEmployeeMessages: (employeeId: string) => {
      return Promise.resolve([
        { messageId: '1', timestamp: new Date().toISOString(), content: `Hello from employee ${employeeId}` },
        { messageId: '2', timestamp: new Date().toISOString(), content: 'Second message' },
      ]);
    },
    updateProductFrequency: (_frequency: string) => {
      return Promise.resolve({ status: 'success' });
    },
    getProductInfo: (_startDate?: string, _endDate?: string) => {
      return Promise.resolve({
        totalFound: 50,
        totalSent: 40,
        shipmentDates: [
          { date: '2024-11-01', found: 10, sent: 8 },
          { date: '2024-11-02', found: 15, sent: 12 },
        ],
      });
    },
    getStoreEmployees: (_storeId: string) => {
      return Promise.resolve([
        { employeeId: 'emp1', name: 'John Doe', position: 'Manager' },
        { employeeId: 'emp2', name: 'Jane Smith', position: 'Cashier' },
      ]);
    },
    getEmployeeSchedule: (employeeId: string) => {
      return Promise.resolve({
        employeeId,
        name: 'John Doe',
        schedule: [
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '00:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },

          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },



          { date: '2024-11-01', shiftStart: '15:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },
          { date: '2024-11-01', shiftStart: '10:00', shiftEnd: '17:00' },

          { date: '2024-11-02', shiftStart: '10:00', shiftEnd: '18:00' },
          { date: '2023-11-01', shiftStart: '15:00', shiftEnd: '17:00' },
        ],
      });
    },
  };
  
  export default mockApi;
  