import type { Meta, StoryObj } from '@storybook/nextjs-vite';
import Button from './index';

const meta = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    variation: {
      options: ['default', 'small'],
      control: { type: 'radio' },
    },
    onClick: { action: 'clicked' },
    text: { control: 'text' },
  },
  args: {
    text: 'Default Button',
    variation: 'default',
    onClick: () => {},
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    text: 'Default Button',
    variation: 'default',
    onClick: () => {},
  },
};

export const Small: Story = {
  args: {
    text: 'Small Button',
    variation: 'small',
    onClick: () => {},
  },
};
