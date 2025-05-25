// components/StoreSettingsModal.tsx
import React, { useState } from "react";
import { Dialog, DialogTitle, DialogContent, DialogActions, TextField, Button } from "@mui/material";

type Props = {
  open: boolean;
  onClose: () => void;
  storeId: string;
  onSuccess?: () => void;
  defaultValues?: { daily_checks_count: number; daily_checks_interval: number };
  updateStoreCheckSettings: (
    storeId: string,
    settings: { daily_checks_count: number; daily_checks_interval: number }
  ) => Promise<unknown>;
};

const StoreSettingsModal: React.FC<Props> = ({ open, onClose, storeId, updateStoreCheckSettings, onSuccess, defaultValues }) => {
  const [dailyChecksCount, setDailyChecksCount] = useState(defaultValues?.daily_checks_count || 1);
  const [dailyChecksInterval, setDailyChecksInterval] = useState(defaultValues?.daily_checks_interval || 1);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      await updateStoreCheckSettings(storeId, {
        daily_checks_count: dailyChecksCount,
        daily_checks_interval: dailyChecksInterval,
      });
      onClose();
      onSuccess?.();
    } catch (err) {
      alert("Ошибка при обновлении настроек");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Настройки периодичности проверки</DialogTitle>
      <DialogContent>
        <TextField
          label="Количество проверок в день"
          type="number"
          fullWidth
          margin="normal"
          value={dailyChecksCount}
          onChange={(e) => setDailyChecksCount(parseInt(e.target.value))}
        />
        <TextField
          label="Интервал между проверками (в часах)"
          type="number"
          fullWidth
          margin="normal"
          value={dailyChecksInterval}
          onChange={(e) => setDailyChecksInterval(parseInt(e.target.value))}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Отмена</Button>
        <Button variant="contained" onClick={handleSubmit} disabled={loading}>
          {loading ? "Сохраняем..." : "Изменить"}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default StoreSettingsModal;
