import { createReducer, on } from '@ngrx/store';
import { Course } from '../services/course.service';
import { loadCourses, loadCoursesSuccess, loadCoursesFailure } from './courses.actions';

export interface CoursesState {
  items: Course[];
  loading: boolean;
  error: string | null;
}

const initialState: CoursesState = { items: [], loading: false, error: null };

export const coursesReducer = createReducer(
  initialState,
  on(loadCourses, (state) => ({ ...state, loading: true, error: null })),
  on(loadCoursesSuccess, (state, { courses }) => ({ ...state, items: courses, loading: false })),
  on(loadCoursesFailure, (state, { error }) => ({ ...state, error, loading: false }))
);

// Data flow: Component -> dispatch(loadCourses) -> Effect listens for loadCourses
// -> calls CourseService (API) -> dispatches loadCoursesSuccess/Failure
// -> Reducer updates State -> Selector reads State -> Component re-renders.
