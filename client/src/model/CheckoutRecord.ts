type CheckoutRecord = {
  checkoutId: number;
  memberId: number;
  itemId: number;
  instanceId: number;
  personnelId: number;
  checkoutDate: Date;
  dueDate: Date;
  returnDate: Date | null;
};
export default CheckoutRecord;
