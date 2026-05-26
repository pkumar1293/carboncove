interface StepIndicatorProps {
  currentStep: number
  labels: string[]
}

export function StepIndicator({ currentStep, labels }: StepIndicatorProps) {
  return (
    <div className="mb-8 w-full">
      <div className="flex items-center justify-between">
        {labels.map((label, i) => {
          const step = i + 1
          const isDone = step < currentStep
          const isActive = step === currentStep
          return (
            <div key={label} className="flex flex-1 flex-col items-center">
              <div className="flex w-full items-center">
                {i > 0 && (
                  <div
                    className={`h-1 flex-1 ${isDone || isActive ? 'bg-primary' : 'bg-border'}`}
                  />
                )}
                <div
                  className={`flex h-9 w-9 items-center justify-center rounded-full border-2 text-sm font-bold ${
                    isDone
                      ? 'border-primary bg-primary text-primary-foreground'
                      : isActive
                        ? 'border-primary bg-card text-primary'
                        : 'border-border bg-card text-muted-foreground'
                  }`}
                >
                  {isDone ? '✓' : step}
                </div>
                {i < labels.length - 1 && (
                  <div className={`h-1 flex-1 ${isDone ? 'bg-primary' : 'bg-border'}`} />
                )}
              </div>
              <span
                className={`mt-1 text-center text-xs ${
                  isActive ? 'font-semibold text-primary' : 'text-muted-foreground'
                }`}
              >
                {label}
              </span>
            </div>
          )
        })}
      </div>
    </div>
  )
}
