import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  formData: {},
};

const chatSlice = createSlice({
  name: "chat",
  initialState,
  reducers: {
    setFormData: (state, action) => {
      state.formData = action.payload;
    },
    clearFormData: (state) => {
      state.formData = {};
    },
  },
});

export const { setFormData, clearFormData } = chatSlice.actions;
export default chatSlice.reducer;