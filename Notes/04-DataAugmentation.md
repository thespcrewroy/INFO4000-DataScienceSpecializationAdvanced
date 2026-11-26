# Data Augmentation

Data augmentation introduces variation and diversity into training data without increasing the size of the dataset on disk or the batch size. Exposing the model to a wider range of possible inputs during training improves its robustness and generalization. The course splits it into structured data (tables) and unstructured data (images, text, and audio).

## Structured Data

**Feature engineering:**

- **Creating new features:** combining existing features to create new ones
- **Transforming features:** applying math transformations, such as a log or square root transformation
- **Encoding categorical features:** converting categories into numbers, such as with one hot encoding or label encoding

**Handling missing values:**

- **Imputation:** replacing missing values with estimates, such as the mean, median, or mode
- **Deletion:** removing rows or columns with missing values, if appropriate

**Handling outliers:**

- **Winsorization:** capping extreme values at a chosen percentile
- **Transformation:** applying transformations, such as a log transformation, to reduce the impact of outliers
- **Standardization:** scaling features to have a mean of 0 and a variance of 1
- **Normalization:** scaling features to a specific range, such as 0 to 1

## Unstructured Data

**Images:**

- **Geometric transformations:** flipping (horizontal or vertical), rotation, cropping, scaling, translation, and shearing
- **Color space adjustments:** brightness, contrast, saturation, and hue
- **Random noise:** Gaussian noise and salt and pepper noise

**Text:**

- **Synonym replacement:** replacing words with their synonyms
- **Back translation:** translating a sentence into another language and then back to the original
- **Random insertion:** inserting random words into a sentence
- **Random deletion:** deleting random words from a sentence
- **Random swap:** swapping the positions of two words in a sentence

**Audio:**

- **Time stretching:** changing the speed without changing the pitch
- **Pitch shifting:** changing the pitch without changing the speed
- **Adding noise:** mixing in background noise
- **Time shifting:** shifting audio samples forward or backward in time

## Guidelines

- **Domain knowledge:** choose augmentation and transformation techniques based on the specific domain and problem. Flipping a photo of a cat still shows a cat, but flipping a digit like 6 can turn it into a 9.
- **Experimentation:** try different techniques and measure their effect on model performance.
- **Balance:** augment enough to improve generalization, but avoid over augmenting, which creates unrealistic training examples.

## Worked Examples

### Scaling Features: Standardization and Normalization

**Standardization** rescales a feature to have a mean of 0 and a standard deviation of 1:

$$
z = \frac{x - \mu}{\sigma}
$$

**Normalization (min max scaling)** rescales a feature to the range $[0, 1]$:

$$
x' = \frac{x - x_{min}}{x_{max} - x_{min}}
$$

**Example:** the feature values $10, 20, 30$ have $\mu = 20$ and $\sigma = \sqrt{\frac{(10-20)^2 + (20-20)^2 + (30-20)^2}{3}} \approx 8.165$

| $x$ | Standardized $z$ | Normalized $x'$ |
|---|---|---|
| 10 | $(10 - 20) / 8.165 \approx -1.225$ | $(10 - 10) / 20 = 0$ |
| 20 | $0$ | $0.5$ |
| 30 | $\approx 1.225$ | $1$ |

**Log transformation** shrinks large values much more than small ones, which reduces skew and the pull of outliers. With $\log_{10}$, the values $10, 100, 1000$ become $1, 2, 3$.
