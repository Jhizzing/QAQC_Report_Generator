# GUI Testing Checklist

## 🎯 Interactive Testing Session

Use this checklist to guide your testing and provide feedback via microphone.

---

## ✅ Pre-Launch Checks

- [ ] Virtual environment activated
- [ ] PyQt6 installed (`pip install PyQt6`)
- [ ] Test data files available in `mock_data/`

---

## 🧪 Testing Areas

### 1. **Visual Appearance & Theme**
- [ ] Text readability (menu bar, buttons, labels)
- [ ] Color contrast (dark text on light backgrounds)
- [ ] Button visibility (not white-on-white)
- [ ] Dialog box styling (OK buttons visible)
- [ ] Overall professional appearance
- [ ] Geological theme consistency

### 2. **Data Import Panel**
- [ ] File selection dialog works
- [ ] CSV/XLSX file loading
- [ ] Data preview table displays correctly
- [ ] Column mapping interface
- [ ] Error messages for invalid files
- [ ] Progress indicators during import

### 3. **Analysis Panel**
- [ ] Analysis options visible and accessible
- [ ] Settings configuration
- [ ] CRM selection (if applicable)
- [ ] Analysis execution
- [ ] Results display

### 4. **Visualization Panel**
- [ ] Plot generation works
- [ ] Plot types available (standards, blanks, duplicates)
- [ ] Plot quality and readability
- [ ] Export functionality
- [ ] Plot interaction (zoom, pan if applicable)

### 5. **Data Flow & Validation**
- [ ] No results generated without data
- [ ] Proper error handling
- [ ] Data validation messages
- [ ] Smooth transitions between panels

### 6. **User Experience**
- [ ] Intuitive navigation
- [ ] Clear instructions/placeholders
- [ ] Responsive interface
- [ ] Professional appearance for geologists

---

## 🐛 Issues to Report

When testing, note:
- **Visual Issues**: Text too light, buttons invisible, poor contrast
- **Functional Issues**: Buttons not working, data not loading, errors
- **UX Issues**: Confusing navigation, unclear instructions
- **Performance Issues**: Slow loading, laggy interface

---

## 📝 Test Data Files

Available test files:
- `mock_data/gui_test_data.csv` - Basic test data
- `mock_data/complex_test_data.csv` - Complex scenarios
- `input/assays.csv` - Real-world format example

---

## 🚀 Launch Command

```bash
python3 launch_gui.py
```

Or for verbose output:
```bash
python3 launch_gui_simple.py
```

---

## 💡 Feedback Format

As you test, provide feedback on:
1. **What you're testing** (e.g., "I'm clicking the Import button")
2. **What you see** (e.g., "The button is white on white")
3. **What you expect** (e.g., "I expect a blue button with white text")
4. **Any errors** (e.g., "I got an error message saying...")

---

**Ready to test!** Launch the GUI and provide real-time feedback! 🎤
