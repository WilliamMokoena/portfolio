import { Component, OnInit, EventEmitter, Output } from '@angular/core'

@Component({
  selector: 'app-tasks-group',
  templateUrl: './tasks-group.component.html',
  styleUrls: ['./tasks-group.component.scss']
})
export class TasksGroupComponent implements OnInit {

  @Output()
  groupClickedEventEmitter: EventEmitter<string> = new EventEmitter<string>()

  constructor() { }

  ngOnInit(): void {
  }

  public groupClicked() {
      this.groupClickedEventEmitter.emit('Group clicked')
  }

}
