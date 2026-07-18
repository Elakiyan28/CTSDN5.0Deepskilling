import { configureStore } from "@reduxjs/toolkit";
import enrollmentReducer from "./features/enrollmentSlice.js";

export const store = configureStore({
  reducer: {
    enrollment: enrollmentReducer,
  },
});
