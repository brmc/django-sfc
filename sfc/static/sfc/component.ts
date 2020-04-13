export class DjangoComponent {
  constructor(cmp: HTMLElement) {
    cmp.querySelectorAll('[data-ref]').forEach(i => {
      // @ts-ignore
      this[i.getAttribute('data-ref')] = i
    })
    this.connectedCallback()
  }

  connectedCallback(): void {
    throw 'Components must implement connectedCallback()'
  }
}

export interface DynamicComponent {
  render(): void
}

class Record {
  constructor(
    public cmp: { new(x: HTMLElement): DjangoComponent },
    public instances: DjangoComponent[]
  ) {}
}

class Registry {
  private static instance: Registry
  private components: { [key: string]: Record } = {}

  private constructor() {
    Registry.instance = this
  }

  static new() {
    return Registry.instance || new Registry()
  }

  registerComponent(
    selector: string,
    component: { new(x: Element): DjangoComponent }
  ) {
    document.addEventListener('DOMContentLoaded', () => {
      document.querySelectorAll(`[data-cmp=${selector}]`).forEach(x => {
        let record = this.components[selector]
        if (!record) {
          record = this.components[selector] = new Record(component, [])
        }
        record.instances.push(new component(x))
      })
    })
  }
}

export const registry = Registry.new()
