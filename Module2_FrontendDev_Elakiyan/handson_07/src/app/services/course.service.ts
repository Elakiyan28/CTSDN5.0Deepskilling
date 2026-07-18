import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';

export interface Course {
  id: number;
  name: string;
  code: string;
  credits: number;
  grade: string;
}

@Injectable({ providedIn: 'root' })
export class CourseService {
  constructor(private http: HttpClient) {}

  getCourses(): Observable<Course[]> {
    return this.http
      .get<any[]>('https://jsonplaceholder.typicode.com/posts?_limit=5')
      .pipe(
        map((posts) =>
          posts.map((p, i) => ({
            id: p.id,
            name: p.title.slice(0, 24),
            code: `CS${100 + i}`,
            credits: 3 + (i % 2),
            grade: ['A', 'A-', 'B+', 'B', 'A'][i],
          }))
        )
      );
  }
}
