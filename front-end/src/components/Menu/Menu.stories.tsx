import type { Meta, StoryObj } from '@storybook/nextjs-vite';
import Menu from './index';

const meta = {
  title: 'Components/Menu',
  component: Menu,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  // No props needed for Menu
} satisfies Meta<typeof Menu>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    isOpen: true,
    onClickBackground: () => alert('Background clicked'),
  },
};
