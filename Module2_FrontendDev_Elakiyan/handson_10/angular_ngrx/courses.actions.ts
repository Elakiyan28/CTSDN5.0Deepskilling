import { createAction, props } from '@ngrx/store';
import { Course } from '../services/course.service';

export const loadCourses = createAction('[Courses Page] Load Courses');
export const loadCoursesSuccess = createAction(
  '[Courses API] Load Courses Success',
  props<{ courses: Course[] }>()
);
export const loadCoursesFailure = createAction(
  '[Courses API] Load Courses Failure',
  props<{ error: string }>()
);
