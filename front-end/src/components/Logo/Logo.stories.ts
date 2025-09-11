import type { Meta, StoryObj } from '@storybook/nextjs-vite';

import Logo from './index';

const meta = {
  title: 'Components/Logo',
  component: Logo,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    size: {
      options: ['default', 'small'],
      control: { type: 'radio' },
    },
  },
  args: {
    size: 'default',
  },
} satisfies Meta<typeof Logo>;

export default meta;
type Story = StoryObj<typeof meta>;

export const LogoStory: Story = {
  args: {
    size: 'default',
  },
  globals: {
    backgrounds: { value: 'dark' },
  },
};
