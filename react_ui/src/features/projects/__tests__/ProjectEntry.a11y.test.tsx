import { describe, expect, it, beforeEach, vi } from 'vitest';
import { axe } from 'jest-axe';
import { render, screen, userEvent } from '../../../test/utils';
import { ProjectEntry } from '../ProjectEntry';
import { useProjectStore } from '../../../stores/projectStore';

vi.mock('../../../stores/projectStore', () => ({
  useProjectStore: vi.fn(),
}));

vi.mock('../../../utils/projectFile', () => ({
  selectProjectFile: vi.fn(),
  loadProjectFromFile: vi.fn(),
}));

describe('ProjectEntry accessibility', () => {
  beforeEach(() => {
    vi.mocked(useProjectStore).mockReturnValue({
      createProject: vi.fn(),
      recentProjects: [],
      openProject: vi.fn(),
      loadFromFile: vi.fn(),
    } as unknown as ReturnType<typeof useProjectStore>);
  });

  it('has no obvious accessibility violations in select mode', async () => {
    const { container } = render(<ProjectEntry />);

    expect(screen.getByRole('heading', { name: /logiqore qaqc reporter/i })).toBeInTheDocument();
    const results = await axe(container);

    expect(results).toHaveNoViolations();
  });

  it('has no obvious accessibility violations in new session form mode', async () => {
    const { container } = render(<ProjectEntry />);

    await userEvent.click(screen.getByRole('button', { name: /new qaqc session/i }));

    expect(screen.getByRole('heading', { name: /new session/i })).toBeInTheDocument();
    const results = await axe(container);

    expect(results).toHaveNoViolations();
  });
});
