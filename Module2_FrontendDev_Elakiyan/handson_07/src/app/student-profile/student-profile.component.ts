import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-student-profile',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './student-profile.component.html',
})
export class StudentProfileComponent {
  profileForm = new FormGroup({
    name: new FormControl('', [Validators.required]),
    email: new FormControl('', [Validators.required, Validators.email]),
    semester: new FormControl('', [
      Validators.required,
      Validators.min(1),
      Validators.max(8),
    ]),
  });

  onSubmit(): void {
    console.log(this.profileForm.value);
  }
}
