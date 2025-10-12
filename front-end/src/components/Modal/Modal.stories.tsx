import type { Meta, StoryObj } from '@storybook/nextjs-vite';
import Modal from './index';

const meta = {
  title: 'Components/Modal',
  component: Modal,
  parameters: {
    layout: 'padded',
    viewport: {
      defaultViewport: 'responsive',
    },
    docs: {
      story: {
        inline: false,
        iframeHeight: 600,
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    isOpen: {
      control: { type: 'boolean' },
      description: 'Controls whether the modal is visible',
    },
    onConfirm: { 
      action: 'confirmed',
      description: 'Callback when confirm button is clicked',
    },
    onCancel: { 
      action: 'cancelled',
      description: 'Callback when cancel/close is triggered',
    },
  },
} satisfies Meta<typeof Modal>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: (args) => <Modal {...args} />,
  args: {
    isOpen: true,
    onConfirm: () => alert('Modal confirmed!'),
    onCancel: () => alert('Modal cancelled!'),
  },
};

export const Closed: Story = {
  render: (args) => <Modal {...args} />,
  args: {
    isOpen: false,
    onConfirm: () => alert('Modal confirmed!'),
    onCancel: () => alert('Modal cancelled!'),
  },
};