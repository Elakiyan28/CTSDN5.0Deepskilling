import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { catchError, map, mergeMap, of } from 'rxjs';
import { CourseService } from '../services/course.service';
import { loadCourses, loadCoursesSuccess, loadCoursesFailure } from './courses.actions';

@Injectable()
export class CoursesEffects {
  loadCourses$ = createEffect(() =>
    this.actions$.pipe(
      ofType(loadCourses),
      mergeMap(() =>
        this.courseService.getCourses().pipe(
          map((courses) => loadCoursesSuccess({ courses })),
          catchError((error) => of(loadCoursesFailure({ error: error.message })))
        )
      )
    )
  );

  constructor(private actions$: Actions, private courseService: CourseService) {}
}

// Angular ErrorHandler (global error handler, Task 3 "for either framework"):
// import { ErrorHandler, Injectable } from '@angular/core';
// @Injectable()
// export class GlobalErrorHandler implements ErrorHandler {
//   handleError(error: unknown) {
//     console.error('Global error:', error);
//     // show fallback UI / toast here
//   }
// }
// Register it in app.config.ts providers: { provide: ErrorHandler, useClass: GlobalErrorHandler }
