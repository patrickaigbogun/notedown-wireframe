
export default function ThemeController() {
	return (
		<label className="flex gap-2 cursor-pointer">
			<span className="text-sm">theme</span>
			<input type="checkbox" value="lemonade" className="toggle theme-controller" />
		</label>
	)
}
