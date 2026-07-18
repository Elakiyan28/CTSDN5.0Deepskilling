# Hands-On 10 — State Management Comparison

| | React + Redux Toolkit | Angular + NgRx | Vue + Pinia |
|---|---|---|---|
| **Boilerplate** | Low — `createSlice` + `createAsyncThunk` generate action types and reducers for you. | Highest — separate files for actions, reducer, effects, selectors even for one feature. | Lowest — a single `defineStore` with refs/computed/actions, close to plain JS. |
| **Learning curve** | Moderate — need to understand actions/reducers/thunks, but Immer hides the immutability pain. | Steepest — requires understanding RxJS operators (`mergeMap`, `catchError`) on top of the Redux pattern. | Gentlest — if you know Vue's Composition API (`ref`, `computed`), Pinia adds almost nothing new. |
| **Built-in tooling** | Redux DevTools (time-travel debugging, action log). | Redux DevTools support via `@ngrx/store-devtools`, plus Angular DevTools. | Vue DevTools has a dedicated Pinia tab showing state/actions live. |
| **Side effects** | Handled inline inside `createAsyncThunk`. | Isolated into `Effects` classes — keeps reducers 100% pure, but adds a file. | Handled inline inside store actions (like Redux Toolkit) — no separate effects layer. |
| **When it shines** | Medium-to-large apps that want structure without excessive ceremony. | Large enterprise apps already committed to Angular's opinionated architecture. | Small-to-medium apps that want minimal setup and fast iteration. |

**Summary:** Redux Toolkit and Pinia both cut boilerplate relative to their
"classic" ancestors (plain Redux, plain Vuex). NgRx keeps the strictest
separation of concerns, which pays off in very large codebases but is
overkill for a project the size of this Student Portal.
