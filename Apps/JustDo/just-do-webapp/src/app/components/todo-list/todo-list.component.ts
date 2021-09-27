import { Component, OnInit } from '@angular/core'

@Component({
  selector: 'app-todo-list',
  templateUrl: './todo-list.component.html',
  styleUrls: ['./todo-list.component.scss']
})

export class TodoListComponent implements OnInit {

  public tasks = [
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
    'Etiam scelerisque rutrum nisl, sed viverra tellus convallis euismod',
    'Phasellus commodo feugiat tortor, ut tempor quam euismod quis',
    'Nam efficitur nisl sit amet porta tristique',
    'Etiam scelerisque rutrum nisl, sed viverra tellus convallis euismod',
    'Phasellus commodo feugiat tortor, ut tempor quam euismod quis',
    'Nam efficitur nisl sit amet porta tristique',
    'Etiam scelerisque rutrum nisl, sed viverra tellus convallis euismod',
    'Phasellus commodo feugiat tortor, ut tempor quam euismod quis'
  ]

  constructor() { }

  ngOnInit(): void {
  }

}
