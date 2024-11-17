import React from 'react';
import { cn } from '../../../utils/cn';
import { AlertTriangle, CheckCircle, XCircle } from 'lucide-react';

export interface AlertProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'success' | 'destructive';
  children?: React.ReactNode;
}

const alertVariants = {
  default: 'border-blue-200 bg-blue-50 text-blue-800',
  success: 'border-green-200 bg-green-50 text-green-800',
  destructive: 'border-red-200 bg-red-50 text-red-800',
};

const alertIcons = {
  default: AlertTriangle,
  success: CheckCircle,
  destructive: XCircle,
};

export const Alert = React.forwardRef<HTMLDivElement, AlertProps>(
  ({ className, variant = 'default', children, ...props }, ref) => {
    const Icon = alertIcons[variant];
    
    return (
      <div
        ref={ref}
        role="alert"
        className={cn(
          "rounded-lg border p-4 flex items-start",
          alertVariants[variant],
          className
        )}
        {...props}
      >
        {Icon && <Icon className="h-5 w-5 mt-0.5 mr-3" />}
        <div>{children}</div>
      </div>
    );
  }
);
Alert.displayName = "Alert";

export const AlertTitle = React.forwardRef<HTMLHeadingElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, children, ...props }, ref) => {
    return (
      <h5
        ref={ref}
        className={cn("mb-1 font-medium tracking-tight", className)}
        {...props}
      >
        {children}
      </h5>
    );
  }
);
AlertTitle.displayName = "AlertTitle";

export const AlertDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn("text-sm opacity-90", className)}
        {...props}
      >
        {children}
      </div>
    );
  }
);
AlertDescription.displayName = "AlertDescription";