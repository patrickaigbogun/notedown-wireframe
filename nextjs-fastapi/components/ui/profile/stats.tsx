import { ArrowsClockwise, MusicNoteSimple, ShareFat } from "@phosphor-icons/react/dist/ssr";

export default function StatsCards() {
    return (
        <section className="px-4 py-8 sm:px-8">
            <div className="max-w-4xl mx-auto">
                <div className="w-full shadow stats stats-vertical lg:stats-horizontal">
                    <div className="stat">
                        <div className="stat-figure text-primary">
                            <ArrowsClockwise size={24} weight="duotone" />
                        </div>
                        <div className="stat-title">Total Sessions</div>
                        <div className="stat-value">89</div>
                        <div className="stat-desc">21% more than last month</div>
                    </div>

                    <div className="stat">
                        <div className="stat-figure text-secondary">
                            <ShareFat size={24} weight="duotone" />
                        </div>
                        <div className="stat-title">Shared Notes</div>
                        <div className="stat-value">47</div>
                        <div className="stat-desc">↗︎ 40 (22%)</div>
                    </div>

                    <div className="stat">
                        <div className="stat-figure text-accent">
                            <MusicNoteSimple size={24} weight="duotone" />
                        </div>
                        <div className="stat-title">Music Notes</div>
                        <div className="stat-value">12</div>
                        <div className="stat-desc">Just added</div>
                    </div>
                </div>
            </div>
        </section>
    )
}
